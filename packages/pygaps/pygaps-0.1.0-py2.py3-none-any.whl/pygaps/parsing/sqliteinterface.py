# %%
"""
This module contains the sql interface for data manipulation
"""

__author__ = 'Paul A. Iacomi'

import array
import sqlite3

import numpy
import pandas

from ..classes.adsorbate import Adsorbate
from ..classes.pointisotherm import PointIsotherm
from ..classes.sample import Sample
from ..utilities.sqlite_utilities import build_delete
from ..utilities.sqlite_utilities import build_insert
from ..utilities.sqlite_utilities import build_select
from ..utilities.sqlite_utilities import build_update


def db_get_samples(pth):
    """
    Gets all samples and their properties

    The number of samples is usually small, so all can be loaded in memory at once
    """

    # Connect to database
    with sqlite3.connect(pth) as db:

        # Set row factory
        db.row_factory = sqlite3.Row
        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        # Execute the query
        cursor.execute('''SELECT * FROM samples''')

        samples = []

        # Create the samples
        for row in cursor:

            sample_params = dict(zip(row.keys(), row))

            # Get the extra data from the sample_properties table
            cur_inner = db.cursor()

            cur_inner.execute(build_select(table='sample_properties',
                                           to_select=['type', 'value'],
                                           where=['sample_id']), {
                'sample_id':        sample_params.get('id')
            })

            sample_params['properties'] = {
                row[0]: row[1] for row in cur_inner}

            # Build sample objects
            samples.append(Sample(sample_params))

    # Close the db connection
    if db:
        db.close()

    # Print success
    print("Selected", len(samples), "samples")

    return samples


def db_upload_sample(pth, sample, overwrite=False):
    """
    Uploads samples to the database
    If overwrite is set to true, the sample is overwritten
    Overwrite is done based on sample.name + sample.batch
    WARNING: Overwrite is done on ALL fields
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            if overwrite:
                sql_com = build_update(table="samples",
                                       to_set=['project', 'struct', 'owner', 'type',
                                               'contact', 'form', 'source_lab', 'comment'],
                                       where=['name', 'batch'])
            else:
                sql_com = build_insert(table="samples",
                                       to_insert=['name', 'batch', 'project', 'struct', 'owner', 'type',
                                                  'contact', 'form', 'source_lab', 'comment'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'name':         sample.name,
                'batch':        sample.batch,
                'owner':        sample.owner,
                'contact':      sample.contact,
                'source_lab':   sample.source_lab,
                'project':      sample.project,
                'struct':       sample.struct,
                'type':         sample.type,
                'form':         sample.form,
                'comment':      sample.comment,
            }
            )

            # Upload or modify data in sample_properties table
            if len(sample.properties) > 0:
                # Get id of sample
                sample_id = cursor.execute(
                    build_select(table='samples',
                                 to_select=['id'],
                                 where=['name', 'batch']), {
                        'name':        sample.name,
                        'batch':       sample.batch,
                    }
                ).fetchone()[0]

                # Sql of update routine
                sql_update = build_update(table='sample_properties',
                                          to_set=['type', 'value'],
                                          where=['sample_id'])
                # Sql of insert routine
                sql_insert = build_insert(table='sample_properties',
                                          to_insert=['sample_id', 'type', 'value'])

                updates = []

                if overwrite:
                    # Find existing properties
                    cursor.execute(
                        build_select(table='sample_properties',
                                     to_select=['type'],
                                     where=['sample_id']), {
                            'sample_id':        sample_id,
                        }
                    )
                    updates = [elt[0] for elt in cursor.fetchall()]

                for prop in sample.properties:
                    if prop in updates:
                        sql_com_prop = sql_update
                    else:
                        sql_com_prop = sql_insert

                    cursor.execute(sql_com_prop, {
                        'sample_id':        sample_id,
                        'type':             prop,
                        'value':            sample.properties[prop]
                    })

        # Print success
        print("Sample uploaded", sample.name, sample.batch)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              sample.name,
              sample.batch,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_sample_type(pth, sample_type):
    "Uploads a sample type"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="sample_type",
                                   to_insert=['nick', 'name'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'nick':         sample_type['nick'],
                'name':         sample_type['name'],
            }
            )

        # Print success
        print("Sample type uploaded", sample_type)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample type:", "\n",
              sample_type['nick'],
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_upload_sample_form(pth, sample_form):
    "Uploads a sample form"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="sample_forms",
                                   to_insert=['nick', 'name', 'desc'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'nick':         sample_form['nick'],
                'name':         sample_form['name'],
                'desc':         sample_form.get('desc'),
            }
            )

        # Print success
        print("Sample form uploaded", sample_form)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample form:", "\n",
              sample_form['nick'],
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_upload_sample_property_type(pth, property_type, property_unit):
    "Uploads a property type"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="sample_properties_type",
                                   to_insert=['type', 'unit'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'type':         property_type,
                'unit':         property_unit,
            }
            )

        # Print success
        print("Property type uploaded", property_type)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              property_type,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_delete_sample(pth, sample):
    """
    Delete experiment to the database
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # Get id of sample
            sample_ids = cursor.execute(
                build_select(table='samples',
                             to_select=['id'],
                             where=['name', 'batch']), {
                    'name':        sample.name,
                    'batch':       sample.batch,
                }
            ).fetchone()

            if sample_ids is None:
                raise sqlite3.IntegrityError(
                    "Sample to delete does not exist in database")

            # Delete data from sample_properties table
            # Build sql request
            sql_com = build_delete(table='sample_properties',
                                   where=['sample_id'])

            cursor.execute(sql_com, {'sample_id': sample_ids[0]})

            # Delete sample info in samples table
            sql_com = build_delete(table='samples',
                                   where=['id'])

            cursor.execute(sql_com, {'id': sample_ids[0]})

            # Print success
            print("Success", sample.name, sample.batch)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              sample.name,
              sample.batch,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_get_experiments(pth, criteria):
    """
    Gets experiments with the selected criteria from the database
    """

    # Connect to database
    with sqlite3.connect(pth) as db:

        # Set row factory
        db.row_factory = sqlite3.Row
        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        # Build SQL request
        sql_com = build_select(table='experiments',
                               to_select=['id', 'date', 'is_real', 'exp_type',
                                          'sample_name', 'sample_batch', 't_act',  't_exp', 'machine',
                                          'gas', 'user', 'lab', 'project',  'comment'],
                               where=criteria.keys())

        # Get experiment info from database
        cursor.execute(sql_com, criteria)

        # Create the isotherms
        isotherms = []

        for row in cursor:
            exp_params = dict(zip(row.keys(), row))
            # TODO remove this
            exp_params['adsorbate'] = exp_params.pop('gas')

            # Get the extra data from the experiment_data table
            cur_inner = db.cursor()

            cur_inner.execute(build_select(table='experiment_data',
                                           to_select=['dtype', 'data'],
                                           where=['exp_id']),
                              {'exp_id': str(exp_params['id'])}
                              )

            # Generate the array for the pandas dataframe
            columns = []
            other_keys = []
            data_arr = None
            for row in cur_inner:
                columns.append(row[0])

                raw = array.array('d', row[1])
                if data_arr is None:
                    data_arr = numpy.expand_dims(numpy.array(raw), axis=1)
                else:
                    data_arr = numpy.hstack(
                        (data_arr, numpy.expand_dims(numpy.array(raw), axis=1)))

            if row[0] not in ('pressure', 'loading'):
                other_keys.append(row[0])

            exp_data = pandas.DataFrame(data_arr, columns=columns)

            # build isotherm object
            isotherms.append(PointIsotherm(exp_data,
                                           pressure_key="pressure",
                                           loading_key="loading",
                                           other_keys=other_keys,
                                           ** exp_params))

    # Close the db connection
    if db:
        db.close()

    # Print success
    print("Selected", len(isotherms), "isotherms")

    return isotherms


def db_upload_experiment(pth, isotherm, overwrite=None):
    """
    Uploads experiment to the database

    Overwrite is the isotherm where the isotherm will be overwritten
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # First, if the goal was to overwrite an isotherm, must delete old data
            if overwrite:
                db_delete_experiment(pth, overwrite)

            # Thenn, the sample is going to be inserted into the database
            # Build SQL request
            sql_com = build_insert(table='experiments',
                                   to_insert=['id', 'date', 'is_real',
                                              'exp_type', 'sample_name', 'sample_batch',
                                              't_act', 't_exp', 'machine',
                                              'gas', 'user', 'lab',
                                              'project', 'comment'])

            # Build upload dict
            upload_dict = {
                'id':               isotherm.id,
                'date':             isotherm.date,
                'is_real':          isotherm.is_real,
                'exp_type':         isotherm.exp_type,
                'sample_name':      isotherm.sample_name,
                'sample_batch':     isotherm.sample_batch,
                't_act':            isotherm.t_act,
                't_exp':            isotherm.t_exp,
                'machine':          isotherm.machine,
                'gas':              isotherm.adsorbate,
                'user':             isotherm.user,
                'lab':              isotherm.lab,
                'project':          isotherm.project,
                'comment':          isotherm.comment
            }

            # Upload experiment info to database
            cursor.execute(sql_com, upload_dict)

            # Then, the isotherm data will be uploaded
            # into the experiment_data table

            # Build sql request
            sql_insert = build_insert(table='experiment_data',
                                      to_insert=['exp_id', 'dtype', 'data'])

            # Insert standard data fields:
            cursor.execute(sql_insert,
                           {'exp_id': isotherm.id, 'dtype': 'pressure',
                            'data': isotherm.pressure().tobytes()}
                           )

            cursor.execute(sql_insert,
                           {'exp_id': isotherm.id, 'dtype': 'loading',
                            'data': isotherm.loading().tobytes()}
                           )

            # Update or insert other fields:
            for key in isotherm.other_keys:
                cursor.execute(sql_insert,
                               {'exp_id': isotherm.id, 'dtype': key,
                                'data': isotherm.other_data(key).tobytes()}
                               )

        # Print success
        print("Success:", isotherm)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on isotherm:", "\n",
              isotherm.exp_type,
              isotherm.sample_name,
              isotherm.sample_batch,
              isotherm.user,
              isotherm.adsorbate,
              isotherm.machine,
              isotherm.t_act,
              isotherm.t_exp,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_experiment_type(pth, experiment_type):
    "Uploads a experiment type"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="experiment_type",
                                   to_insert=['nick', 'name'])

            # Upload or modify data in experiment table
            cursor.execute(sql_com, {
                'nick':         experiment_type['nick'],
                'name':         experiment_type['name'],
            }
            )

        # Print success
        print("Experiment type uploaded", experiment_type['nick'])

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on experiment type:", "\n",
              experiment_type['nick'],
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_upload_experiment_data_type(pth, data_type, data_unit):
    "Uploads a data type"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="experiment_data_type",
                                   to_insert=['type', 'unit'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'type':         data_type,
                'unit':         data_unit,
            }
            )

        # Print success
        print("Data type uploaded", data_type)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              data_type,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_delete_experiment(pth, isotherm):
    """
    Delete experiment to the database
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # Check if sample exists
            ids = cursor.execute(
                build_select(table='experiments',
                             to_select=['id'],
                             where=['id']),
                {'id':        isotherm.id}
            ).fetchone()

            if ids is None:
                raise sqlite3.IntegrityError(
                    "Experiment to delete does not exist in database")

            # Delete data from experiment_data table
            cursor.execute(build_delete(table='experiment_data',
                                        where=['exp_id']), {'exp_id': isotherm.id})

            # Delete experiment info in experiments table
            cursor.execute(build_delete(table='experiments',
                                        where=['id']), {'id': isotherm.id})

            # Print success
            print("Success:", isotherm)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on isotherm:", "\n",
              isotherm.exp_type,
              isotherm.sample_name,
              isotherm.sample_batch,
              isotherm.user,
              isotherm.adsorbate,
              isotherm.machine,
              isotherm.t_act,
              isotherm.t_exp,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_experiment_calculated(pth, data, overwrite=False):
    """
    Uploads an experiment calculated value to be stored in the database
    (such as initial enthalpy of adsorption, henry constant etc)
    Specify overwrite to write on top of existing values
    """
    # Build sql request
    if overwrite:
        sql_com = build_update(table='experiment_calculated',
                               to_set=['henry_c', 'enth_init'],
                               where=['exp_id'])

    else:
        sql_com = build_insert(table='experiment_calculated',
                               to_insert=['exp_id', 'henry_c', 'enth_init'])

    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(pth)

        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        # Upload data to database
        cursor.execute(sql_com, {
            'exp_id':         data['exp_id'],
            'henry_c':        data['henry_c'],
            'enth_init':      data['enth_init']
        }
        )

        # Commit the change
        db.commit()

        # Print success
        print("Calculated data uploaded")

    # Catch the exception
    except sqlite3.IntegrityError as e:
        # Roll back any change if something goes wrong
        db.rollback()
        print("Error on id:", "\n",
              data['exp_id'],
              "\n", e)
        raise e

    finally:
        # Close the db connection
        db.close()

    return


def db_get_gasses(pth):
    """
    Gets all gasses and their properties

    The number of gasses is usually small, so all can be loaded in memory at once
    """

    # Connect to database
    with sqlite3.connect(pth) as db:

        # Set row factory
        db.row_factory = sqlite3.Row
        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')

        # Get required gas from database
        cursor.execute('''SELECT * FROM gasses''')

        gasses = []

        # Create the gasses
        for row in cursor:

            gas_params = dict(zip(row.keys(), row))

            # Get the extra data from the gas_properties table
            cur_inner = db.cursor()

            cur_inner.execute(build_select(table='gas_properties',
                                           to_select=['type', 'value'],
                                           where=['gas_id']), {
                'gas_id': gas_params.get('id')
            })

            gas_params['properties'] = {
                row[0]: row[1] for row in cur_inner}

            # Build gas objects
            gasses.append(Adsorbate(gas_params))

    # Close the db connection
    if db:
        db.close()

    # Print success
    print("Selected", len(gasses), "gasses")

    return gasses


def db_upload_gas(pth, adsorbate, overwrite=False):
    """
    Uploads gasses to the database
    If overwrite is set to true, the gas is overwritten
    Overwrite is done based on gas.name
    WARNING: Overwrite is done on ALL fields
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            if overwrite:
                sql_com = build_update(table="gasses",
                                       to_set=['formula'],
                                       where=['nick'])
            else:
                sql_com = build_insert(table="gasses",
                                       to_insert=['nick', 'formula'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'nick':         adsorbate.name,
                'formula':      adsorbate.formula,
            }
            )

            # Upload or modify data in sample_properties table
            if len(adsorbate.properties) > 0:
                # Get id of gas
                gas_id = cursor.execute(
                    build_select(table='gasses',
                                 to_select=['id'],
                                 where=['nick']), {
                        'nick':         adsorbate.name,
                        'formula':      adsorbate.formula,
                    }
                ).fetchone()[0]

                # Sql of update routine
                sql_update = build_update(table='gas_properties',
                                          to_set=['type', 'value'],
                                          where=['gas_id'])
                # Sql of insert routine
                sql_insert = build_insert(table='gas_properties',
                                          to_insert=['gas_id', 'type', 'value'])

                updates = []

                if overwrite:
                    # Find existing properties
                    cursor.execute(
                        build_select(table='gas_properties',
                                     to_select=['type'],
                                     where=['gas_id']), {
                            'gas_id':        gas_id,
                        }
                    )
                    updates = [elt[0] for elt in cursor.fetchall()]

                for prop in adsorbate.properties:
                    if prop in updates:
                        sql_com_prop = sql_update
                    else:
                        sql_com_prop = sql_insert

                    cursor.execute(sql_com_prop, {
                        'gas_id':           gas_id,
                        'type':             prop,
                        'value':            adsorbate.properties[prop]
                    })

        # Print success
        print("Adsorbate uploaded", adsorbate.name)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              adsorbate.name,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_gas_property_type(pth, property_type, property_unit):
    "Uploads a property type"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="gas_properties_type",
                                   to_insert=['type', 'unit'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'type':         property_type,
                'unit':         property_unit,
            }
            )

        # Print success
        print("Property type uploaded", property_type)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              property_type,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_delete_gas(pth, adsorbate):
    """
    Delete experiment to the database
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # Get id of gas
            ids = cursor.execute(
                build_select(table='gasses',
                             to_select=['id'],
                             where=['nick']),
                {'nick':        adsorbate.name}
            ).fetchone()

            if ids is None:
                raise sqlite3.IntegrityError(
                    "Adsorbate to delete does not exist in database")
            gas_id = ids[0]

            # Delete data from gas_properties table
            # Build sql request
            sql_com = build_delete(table='gas_properties',
                                   where=['gas_id'])

            cursor.execute(sql_com, {'gas_id': gas_id})

            # Delete sample info in labs table
            sql_com = build_delete(table='gasses',
                                   where=['id'])

            cursor.execute(sql_com, {'id': gas_id})

            # Print success
            print("Success", adsorbate.name)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              adsorbate.name,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_contact(pth, contact_dict, overwrite=False):
    """
    Uploads cpmtact to the database
    If overwrite is set to true, the contact is overwritten
    WARNING: Overwrite is done on ALL fields
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            if overwrite:
                sql_com = build_update(table="contacts",
                                       to_set=['name', 'email', 'phone',
                                               'labID', 'type', 'permanent'],
                                       where=['nick'])
            else:
                sql_com = build_insert(table="contacts",
                                       to_insert=['nick', 'name', 'email', 'phone', 'labID', 'type', 'permanent'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'nick':          contact_dict.get('nick'),
                'name':          contact_dict.get('name'),
                'email':         contact_dict.get('email'),
                'phone':         contact_dict.get('phone'),
                'labID':         contact_dict.get('labID'),
                'type':          contact_dict.get('type'),
                'permanent':     contact_dict.get('permanent'),
            }
            )

        # Print success
        print("Contact uploaded", contact_dict.get('nick'))

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on contact:", "\n",
              contact_dict.get('nick'),
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_delete_contact(pth, contact_nick):
    """
    Delete contact in the database
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # Check if contact exists
            ids = cursor.execute(
                build_select(table='contacts',
                             to_select=['nick'],
                             where=['nick']),
                {'nick':        contact_nick}
            ).fetchone()

            if ids is None:
                raise sqlite3.IntegrityError(
                    "Contact to delete does not exist in database")

            sql_com = build_delete(table='contacts',
                                   where=['nick'])

            cursor.execute(sql_com, {'nick': contact_nick})

            # Print success
            print("Success", contact_nick)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on sample:", "\n",
              contact_nick,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_lab(pth, lab_dict, overwrite=False):
    """
    Uploads lab to the database
    If overwrite is set to true, the lab is overwritten
    WARNING: Overwrite is done on ALL fields
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            if overwrite:
                sql_com = build_update(table="labs",
                                       to_set=['name', 'address'],
                                       where=['nick'])
            else:
                sql_com = build_insert(table="labs",
                                       to_insert=['nick', 'name', 'address'])

            # Upload or modify data in labs table
            cursor.execute(sql_com, {
                'nick':         lab_dict.get('nick'),
                'name':         lab_dict.get('name'),
                'address':      lab_dict.get('address'),
            }
            )

        # Print success
        print("Lab uploaded", lab_dict.get('nick'))

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on lab:", "\n",
              lab_dict.get('nick'),
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_delete_lab(pth, lab_nick):
    """
    Delete lab in the database
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # Check if lab exists
            ids = cursor.execute(
                build_select(table='labs',
                             to_select=['nick'],
                             where=['nick']),
                {'nick':        lab_nick}
            ).fetchone()

            if ids is None:
                raise sqlite3.IntegrityError(
                    "Lab to delete does not exist in database")

            sql_com = build_delete(table='labs',
                                   where=['nick'])

            cursor.execute(sql_com, {'nick': lab_nick})

            # Print success
            print("Success", lab_nick)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on lab:", "\n",
              lab_nick,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_machine(pth, machine_dict, overwrite=False):
    """
    Uploads machine to the database
    If overwrite is set to true, the machine is overwritten
    WARNING: Overwrite is done on ALL fields
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            if overwrite:
                sql_com = build_update(table="machines",
                                       to_set=['name', 'type'],
                                       where=['nick'])
            else:
                sql_com = build_insert(table="machines",
                                       to_insert=['nick', 'name', 'type'])

            # Upload or modify data in machines table
            cursor.execute(sql_com, {
                'nick':         machine_dict.get('nick'),
                'name':         machine_dict.get('name'),
                'type':         machine_dict.get('type'),
            }
            )

        # Print success
        print("Machine uploaded", machine_dict.get('nick'))

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on machine:", "\n",
              machine_dict.get('nick'),
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return


def db_upload_machine_type(pth, machine_type):
    "Uploads a machine type"

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            sql_com = build_insert(table="machine_type",
                                   to_insert=['type'])

            # Upload or modify data in sample table
            cursor.execute(sql_com, {
                'type':         machine_type,
            }
            )

        # Print success
        print("Machine type uploaded", machine_type)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on machine type:", "\n",
              machine_type,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()


def db_delete_machine(pth, machine_nick):
    """
    Delete machine in the database
    """

    # Connect to database
    db = sqlite3.connect(pth)
    try:
        with db:
            # Get a cursor object
            cursor = db.cursor()
            cursor.execute('PRAGMA foreign_keys = ON')

            # Check if machine exists
            ids = cursor.execute(
                build_select(table='machines',
                             to_select=['nick'],
                             where=['nick']),
                {'nick':        machine_nick}
            ).fetchone()

            if ids is None:
                raise sqlite3.IntegrityError(
                    "Machine to delete does not exist in database")

            sql_com = build_delete(table='machines',
                                   where=['nick'])

            cursor.execute(sql_com, {'nick': machine_nick})

            # Print success
            print("Success", machine_nick)

    # Catch the exception
    except sqlite3.IntegrityError as e:
        print("Error on machine:", "\n",
              machine_nick,
              "\n", e)
        raise e

    # Close the db connection
    if db:
        db.close()

    return
