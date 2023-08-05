#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 22:15:52 2017

@author: nightowl
"""

from __future__ import print_function
from sql_connector import DVH_SQL
from dicom_to_python import DVHTable, PlanRow, BeamTable, RxTable
import os
import dicom


class DICOM_FileSet:
    def __init__(self, plan, structure, dose):
        self.plan = plan
        self.structure = structure
        self.dose = dose


def dicom_to_sql(**kwargs):
    # Read SQL configuration file
    script_dir = os.path.dirname(__file__)
    rel_path = "preferences/import_settings.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as document:
        import_settings = {}
        for line in document:
            line = line.split()
            if not line:
                continue
            import_settings[line[0]] = line[1:][0]
            # Convert strings to boolean
            if line[1:][0].lower() == 'true':
                import_settings[line[0]] = True
            elif line[1:][0].lower() == 'false':
                import_settings[line[0]] = False

    if 'start_path' in kwargs and kwargs['start_path']:
        rel_path = kwargs['start_path']
        abs_file_path = os.path.join(script_dir, rel_path)
        import_settings['inbox'] = abs_file_path

    sqlcnx = DVH_SQL()
    force_update = False
    if 'force_update' in kwargs and kwargs['force_update']:
        force_update = True
    file_paths, warning = get_file_paths(import_settings['inbox'], force_update=force_update)

    if not warning['mrn']:
        for f in file_paths.itervalues():
            print(f.structure)
            print(f.plan)
            print(f.dose)

            plan = PlanRow(f.plan, f.structure, f.dose)
            if not hasattr(dicom.read_file(f.plan), 'BrachyTreatmentType'):
                beams = BeamTable(f.plan)
            dvhs = DVHTable(f.structure, f.dose)
            rxs = RxTable(f.plan, f.structure)

            setattr(dvhs, 'ptv_number', rank_ptvs_by_D95(dvhs))

            sqlcnx.insert_plan(plan)
            if not hasattr(dicom.read_file(f.plan), 'BrachyTreatmentType'):
                sqlcnx.insert_beams(beams)
            sqlcnx.insert_dvhs(dvhs)
            sqlcnx.insert_rxs(rxs)

            # Default behavior is to move files from inbox to imported
            # Only way to prevent moving files is to set move_files = False in kwargs
            if 'move_files' not in kwargs:
                move_files_to_imported_path(f, import_settings['imported'])
            elif kwargs['move_files']:
                move_files_to_imported_path(f, import_settings['imported'])

            # Default behavior is to organize files in the imported folder
            # Only way to prevent organizing files is to set organize_files = False in kwargs
            if 'organize_files' not in kwargs or kwargs['organize_files']:
                organize_dicom_files(import_settings['imported'])

        # Move remaining files, if any
        if 'move_files' not in kwargs:
            move_all_files(import_settings['imported'], import_settings['inbox'])
            remove_empty_folders(import_settings['inbox'])
        elif kwargs['move_files']:
            move_all_files(import_settings['imported'], import_settings['inbox'])
            remove_empty_folders(import_settings['inbox'])

        if 'organize_files' not in kwargs or kwargs['organize_files']:
            organize_dicom_files(os.path.join(import_settings['imported'], 'misc'))

    else:
        print("FAILURE: Multiple instances of a file type found for the same Study Instance UID")
        print("You may only import one RT Dose, RT Structure, and RT Plan file each for a given UID")
        for i in range(0, len(warning['mrn'])):
            print(warning['mrn'][i], warning['file_type'][i], warning['uid'][i], sep=' ')
        print("Please remove these files from the inbox")

    sqlcnx.cnx.close()


def get_file_paths(start_path, **kwargs):

    f = []
    for root, dirs, files in os.walk(start_path, topdown=False):
        for name in files:
            f.append(os.path.join(root, name))

    plan_files = []
    study_uid_plan = []
    structure_files = []
    study_uid_structure = []
    dose_files = []
    study_uid_dose = []
    warning = {'mrn': [], 'uid': [], 'file_type': []}

    if 'force_update' in kwargs and kwargs['force_update']:
        print('WARNING: Forcing all dicom to be imported (i.e., not checking DB for potential duplicates)')

    db_entry_found = False
    for x in range(0, len(f)):
        if 'force_update' in kwargs and kwargs['force_update']:
            try:
                dicom_file = dicom.read_file(f[x])
                if dicom_file.Modality.lower() == 'rtplan':
                    if dicom_file.StudyInstanceUID in study_uid_plan:
                        warning['mrn'].append = dicom_file.PatientID
                        warning['uid'].append = dicom_file.StudyInstanceUID
                        warning['file_type'].append = 'rtplan'
                    else:
                        plan_files.append(f[x])
                        study_uid_plan.append(dicom_file.StudyInstanceUID)
                elif dicom_file.Modality.lower() == 'rtstruct':
                    if dicom_file.StudyInstanceUID in structure_files:
                        warning['mrn'].append = dicom_file.PatientID
                        warning['uid'].append = dicom_file.StudyInstanceUID
                        warning['file_type'].append = 'rtstruct'
                    else:
                        structure_files.append(f[x])
                        study_uid_structure.append(dicom_file.StudyInstanceUID)
                elif dicom_file.Modality.lower() == 'rtdose':
                    if dicom_file.StudyInstanceUID in dose_files:
                        warning['mrn'].append = dicom_file.PatientID
                        warning['uid'].append = dicom_file.StudyInstanceUID
                        warning['file_type'].append = 'rtdose'
                    else:
                        dose_files.append(f[x])
                        study_uid_dose.append(dicom_file.StudyInstanceUID)
            except Exception:
                pass
        else:
            try:
                if not is_file_imported(f[x]):
                    dicom_file = dicom.read_file(f[x])
                    if dicom_file.Modality.lower() == 'rtplan':
                        if dicom_file.StudyInstanceUID in study_uid_plan:
                            warning['mrn'].append = dicom_file.PatientID
                            warning['uid'].append = dicom_file.StudyInstanceUID
                            warning['file_type'].append = 'rtplan'
                        else:
                            plan_files.append(f[x])
                            study_uid_plan.append(dicom_file.StudyInstanceUID)
                    elif dicom_file.Modality.lower() == 'rtstruct':
                        if dicom_file.StudyInstanceUID in structure_files:
                            warning['mrn'].append = dicom_file.PatientID
                            warning['uid'].append = dicom_file.StudyInstanceUID
                            warning['file_type'].append = 'rtstruct'
                        else:
                            structure_files.append(f[x])
                            study_uid_structure.append(dicom_file.StudyInstanceUID)
                    elif dicom_file.Modality.lower() == 'rtdose':
                        if dicom_file.StudyInstanceUID in dose_files:
                            warning['mrn'].append = dicom_file.PatientID
                            warning['uid'].append = dicom_file.StudyInstanceUID
                            warning['file_type'].append = 'rtdose'
                        else:
                            dose_files.append(f[x])
                            study_uid_dose.append(dicom_file.StudyInstanceUID)
                else:
                    if not db_entry_found:
                        print("The following files are already imported. Must delete from database before reimporting.")
                        print("These files have been moved into the 'misc' folder within your 'imported' folder.")
                        db_entry_found = True
                    print(f[x])
            except Exception:
                pass

    dicom_files = {}
    for a in range(0, len(plan_files)):
        rt_plan = plan_files[a]
        for b in range(0, len(structure_files)):
            if study_uid_plan[a] == study_uid_structure[b]:
                rt_structure = structure_files[b]
        for c in range(0, len(dose_files)):
            if study_uid_plan[a] == study_uid_dose[c]:
                rt_dose = dose_files[c]
        dicom_files[a] = DICOM_FileSet(rt_plan, rt_structure, rt_dose)

    return dicom_files, warning


def rebuild_database(start_path):
    print('connecting to SQL DB')
    sqlcnx = DVH_SQL()
    print('connection established')

    sqlcnx.reinitialize_database()
    print('DB reinitialized with no data')
    dicom_to_sql(start_path=start_path,
                 force_update=True,
                 move_files=False,
                 organize_files=False)
    sqlcnx.cnx.close()


def is_file_imported(file_path):

    try:
        dicom_data = dicom.read_file(file_path)
        uid = dicom_data.StudyInstanceUID
    except Exception:
        return False

    if dicom_data.Modality.lower() == 'rtplan':
        table_name = 'Plans'
    elif dicom_data.Modality.lower() == 'rtstruct':
        table_name = 'DVHs'
    elif dicom_data.Modality.lower() == 'rtdose':
        table_name = 'DVHs'
    else:
        return False

    if DVH_SQL().is_study_instance_uid_in_table(table_name, uid):
        return True
    else:
        return False


def rank_ptvs_by_D95(dvhs):
    ptv_number_list = []
    ptv_index = []

    for i in range(0, dvhs.count):
        ptv_number_list.append(0)
        if dvhs.roi_type[i] == 'PTV':
            ptv_index.append(i)

    ptv_count = len(ptv_index)

    # Calculate D95 for each PTV
    doses_to_rank = get_dose_to_volume(dvhs, ptv_index, 0.95)
    order_index = sorted(range(ptv_count), key=lambda k: doses_to_rank[k])
    final_order = sorted(range(ptv_count), key=lambda k: order_index[k])

    for i in range(0, ptv_count):
        ptv_number_list[ptv_index[i]] = final_order[i] + 1

    return ptv_number_list


def get_dose_to_volume(dvhs, indices, roi_fraction):
    # Not precise (i.e., no interpolation) but good enough for sorting PTVs
    doses = []
    for x in indices:
        abs_volume = dvhs.volume[x] * roi_fraction
        dvh = dvhs.dvhs[x]
        dose = next(x[0] for x in enumerate(dvh) if x[1] < abs_volume)
        doses.append(dose)

    return doses


def move_files_to_imported_path(file_paths, imported_path):
    for file_type in file_paths.__dict__:
        file_path = getattr(file_paths, file_type)
        file_name = file_path.split('/')[-1]
        new = '/'.join([imported_path, file_name])
        try:
            os.rename(file_path, new)
        except:
            os.mkdir(imported_path)
            os.rename(file_path, new)


def organize_dicom_files(path):
    initial_path = os.path.dirname(os.path.realpath(__file__))

    os.chdir(path)

    files = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]

    for i in range(0, len(files)):
        try:
            name = dicom.read_file(files[i]).PatientName.replace(' ', '_').replace('^', '_')
            if not os.path.isdir(name):
                os.mkdir(name)
            file_name = files[i].split('/')[-1]

            old = files[i]
            new = '/'.join([path, name, file_name])
            print(old, new, sep=' ')
            os.rename(old, new)
        except:
            pass

    os.chdir(initial_path)


def remove_empty_folders(start_path):
    if start_path[0:2] == './':
        script_dir = os.path.dirname(__file__)
        rel_path = start_path[2:]
        start_path = os.path.join(script_dir, rel_path)

    for (path, dirs, files) in os.walk(start_path, topdown=False):
        if files:
            continue
        try:
            if path != start_path:
                os.rmdir(path)
        except OSError:
            pass


def move_all_files(new_dir, old_dir):
    initial_path = os.path.dirname(os.path.realpath(__file__))

    os.chdir(old_dir)

    file_paths = []
    for path, subdirs, files in os.walk(old_dir):
        for name in files:
            file_paths.append(os.path.join(path, name))

    misc_path = '/'.join([new_dir, 'misc'])
    if not os.path.isdir(misc_path):
        os.mkdir(misc_path)

    for f in file_paths:
        file_name = f.split('/')[-1]
        new = '/'.join([misc_path, file_name])
        os.rename(f, new)

    os.chdir(initial_path)


if __name__ == '__main__':
    DVH_SQL().reinitialize_database()
    dicom_to_sql()
