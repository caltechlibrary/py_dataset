#!/usr/bin/env python3
import sys
import os
import shutil
import json,csv
from pathlib import Path
from py_dataset import dataset

# Set this to false to aggregate test results, True
# will stop test on first failure.
fail_fast = True

#
# test_basic(c_name) runs tests on basic CRUD ops
# 
def test_basic(t, c_name):
    '''test_basic(c_name) runs tests on basic CRUD ops'''
    # Setup a test record
    key = "2488"
    # NOTE: the JSON stored should have a key/id field if you need that,
    # as of dataset v2 this is no longer injected.
    value = { "key": key, "title": "Twenty Thousand Leagues Under the Seas: An Underwater Tour of the World", "formats": ["epub","kindle","plain text"], "authors": [{ "given": "Jules", "family": "Verne" }], "url": "https://www.gutenberg.org/ebooks/2488"}
    
    # We should have an empty collection, we will create our test record.
    if dataset.create(c_name, key, value) == False:
        err = dataset.error_message()
        t.error(f'create({c_name}, {key}, {value}) failed, {err}')
        return 
    
    # Check to see that we have only one record
    key_count = dataset.count(c_name)
    if key_count != 1:
        t.error(f"Failed, expected count to be 1, got {key_count}")
    
    # Do a minimal test to see if the record looks like it has content
    keyList = dataset.keys(c_name)
    rec, err = dataset.read(c_name, key)
    if err != "":
        t.error(f"Unexpected error for {key} in {c_name}, {err}")
    for k, v in value.items():
       if not isinstance(v, list):
            if k in rec and rec[k] == v:
                t.print("OK, found", k, " -> ", v)
            else:
                t.error(f"epxected {rec[k]} got {v}")
       else:
            if k == "formats" or k == "authors":
                t.print("OK, expected lists for", k, " -> ", v)
            else:
                t.error(f"Failed, expected {k} with list v, got {v}")
    
    # Test updating record
    value["verified"] = True
    if dataset.update(c_name, key, value) == False:
       err = dataset.error_message()
       t.error(f"update({c_name}, {key}, {value}) failed, {err}")
    rec, err = dataset.read(c_name, key)
    if err != "":
        t.error(f"Unexpected error for {key} in {c_name}, {err}")
    for k, v in value.items():
       if not isinstance(v, list):
           if k in rec and rec[k] == v:
               t.print("OK, found", k, " -> ", v)
           else:
               t.error("expected {rec[k]} got {v} for key {k}")
       else:
           if k == "formats" or k == "authors":
               t.print("OK, expected lists for", k, " -> ", v)
           else:
               t.error("Failed, expected {k} with a list for v, got {v}")
    
    # Test path to record
    cwd = f"{Path('.').resolve()}"
    expected_s = "/".join([cwd, c_name, "pairtree", "24", "88", (key+".json")])
    expected_l = len(expected_s)
    p = dataset.path(c_name, key)
    if len(p) != expected_l:
        t.error("Failed, expected length", expected_l, "got", len(p))
    if p != expected_s:
        t.error("Failed, expected", expected_s, "got", p)

    # Test listing records
    l = dataset.list(c_name, [key])
    if len(l) != 1:
        t.error(f"list({c_name}, [{key}]) failed, list should return an array of one record, got", l)
        return

    # test deleting a record
    if dataset.delete(c_name, key) == False:
        err = dataset.error_message()
        t.error("Failed, could not delete record", key, ", ", err)
    

#
# test_keys(t, c_name) test getting, filter and sorting keys
#
def test_keys(t, c_name):
    '''test_keys(c_name) test getting, filter and sorting keys'''
    # Test count after delete
    key_list = dataset.keys(c_name)
    cnt = dataset.count(c_name)
    if cnt != 0:
        t.error("Failed, expected zero records, got", cnt, key_list)
    
    #
    # Generate multiple records for collection for testing keys
    #
    test_records = {
        "gutenberg:21489": {"title": "The Secret of the Island", "formats": ["epub","kindle", "plain text", "html"], "authors": [{"given": "Jules", "family": "Verne"}], "url": "http://www.gutenberg.org/ebooks/21489", "categories": "fiction, novel"},
        "gutenberg:2488": { "title": "Twenty Thousand Leagues Under the Seas: An Underwater Tour of the World", "formats": ["epub","kindle","plain text"], "authors": [{ "given": "Jules", "family": "Verne" }], "url": "https://www.gutenberg.org/ebooks/2488", "categories": "fiction, novel"},
        "gutenberg:21839": { "title": "Sense and Sensibility", "formats": ["epub", "kindle", "plain text"], "authors": [{"given": "Jane", "family": "Austin"}], "url": "http://www.gutenberg.org/ebooks/21839", "categories": "fiction, novel" },
        "gutenberg:3186": {"title": "The Mysterious Stranger, and Other Stories", "formats": ["epub","kindle", "plain text", "html"], "authors": [{ "given": "Mark", "family": "Twain"}], "url": "http://www.gutenberg.org/ebooks/3186", "categories": "fiction, short story"},
        "hathi:uc1321060001561131": { "title": "A year of American travel - Narrative of personal experience", "formats": ["pdf"], "authors": [{"given": "Jessie Benton", "family": "Fremont"}], "url": "https://babel.hathitrust.org/cgi/pt?id=uc1.32106000561131;view=1up;seq=9", "categories": "non-fiction, memoir" }
    }
    test_count = len(test_records)
    
    for k in test_records:
        v = test_records[k]
        # NOTE: in dataset v2 key's are NOT injected into object,
        # so we need to inject a key/id ourselves.
        v['key'] = k
        if dataset.create(c_name, k, v) == False:
            err = dataset.error_message()
            t.error("Failed, could not add", k, "to", c_name, ', ', err)
    
    # Test keys
    all_keys = dataset.keys(c_name)
    if len(all_keys) != test_count:
        t.error("Expected", test_count,"all_keys back, got", keys)
    
# test_issue12() https://github.com/caltechlibrary/py_dataset/issues/12
# delete_frame() returns True but frame metadata still in memory.
#
def test_issue12(t, c_name):
    src = '''[
{"id": "1", "c1": 1, "c2": 2, "c3": 3 },
{"id": "2", "c1": 2, "c2": 2, "c3": 3 },
{"id": "3", "c1": 3, "c2": 3, "c3": 3 },
{"id": "4", "c1": 1, "c2": 1, "c3": 1 },
{"id": "5", "c1": 6, "c2": 6, "c3": 6 }
]'''
    #dataset.verbose_on() # DEBUG
    #dataset.use_strict_dotpath(True) # DEBUG
    if dataset.status(c_name) == False:
        if dataset.init(c_name, "") == False:
            err = dataset.error_message()
            t.error(f'failed to create {c_name}')
            return 
    objects = json.loads(src)
    for obj in objects:
        key = obj['id']
        if dataset.has_key(c_name, key):
            dataset.update(c_name, key, obj)
        else:            
            dataset.create(c_name, key, obj)
    f_names = dataset.frame_names(c_name)
    for f_name in f_names:
        ok = dataset.delete_frame(c_name, f_name)
        if ok == False:
            err = dataset.error_message()
            t.error(f'Failed to delete {f_name} from {c_name} -> "{err}"')
            return
        if dataset.has_frame(c_name, f_name) == True:
            t.error(f'Failed to delete frame {c_name} from {c_name}, frame still exists')
            return
    f_name = 'issue12'
    dot_paths = [ ".c1", "c3" ]
    labels = [ ".col1", ".col3" ]
    keys = dataset.keys(c_name)
    if not dataset.frame_create(c_name, f_name, keys, dot_paths, labels):
        err = dataset.error_message()
        t.error(f'failed to create {f_name} from {c_name}, {err}')
    if not dataset.has_frame(c_name, f_name):
        err = dataset.error_message()
        t.error(f'expected frame {f_name} to exists, {err}')
        return
    f_keys = dataset.frame_keys(c_name, f_name)
    if len(f_keys) == 0:
        err = dataset.error_message()
        t.error(f'expected keys in {f_name}, got zero, {err}')
        return
    f_objects = dataset.frame_objects(c_name, f_name)
    if len(f_objects) == 0:
        err = dataset.error_message()
        t.error(f'expected objects in {f_name}, got zero, {err}')
        return
    if not dataset.delete_frame(c_name, f_name):
        err = dataset.error_message()
        t.error(f'expected to delete {f_name} in {c_name}, {err}')



#
# test_issue32() make sure issue 32 stays fixed.
#
def test_issue32(t, c_name):
    if dataset.create(c_name, "k1", {"id": "k1", "one":1}) == False:
        err = dataset.error_message()
        t.error("Failed to create k1 in", c_name, ', ', err)
        return
    if dataset.has_key(c_name, "k1") == False:
        t.error("Failed, has_key k1 should return", True)
    if dataset.has_key(c_name, "k2") == True:
        t.error("Failed, has_key k2 should return", False)

# Setup our test collection, recreate it if necessary
def test_setup(t, c_name):
    if os.path.exists(c_name):
        shutil.rmtree(c_name)
    if dataset.init(c_name, "") == False:
        err = dataset.error_message()
        t.error("init({c_name}, '') failed, {err}")
        return


def test_check_repair(t, c_name):
    t.print("Testing status on", c_name)
    # Make sure we have a left over collection to check and repair
    if os.path.exists(c_name) == True:
        shutil.rmtree(c_name)
    if dataset.status(c_name) == True:
        dataset.close(c_name)
    if dataset.init(c_name, "") == False:
        err = dataset.error_message()
        t.error(f'init({c_name}, "") failed, {err}')
        return
    if dataset.status(c_name) == False:
        t.error(f"Failed, expected dataset.status() == True, got False for {c_name}")
        return

    if dataset.has_key(c_name, 'one') == False:
        if dataset.create(c_name, 'one', {'id': 'one', "one": 1}) == False:
            err = dataset.error_message()
            t.error(f'create({c_name}, "one", {"id": "one", "one": 1}) failed, {err}')
    t.print(f"Testing check on {c_name}")
    # Check our collection
    if not (dataset.check(c_name) == True):
        err = dataset.error_message()
        t.error("Failed, (before break) expected check True, got False for {c_name} (err: {err})")
        return

    # Break and recheck our collection
    print(f"Removing {c_name}/collection.json to cause a fail")
    if os.path.exists(c_name + "/collection.json"):
        os.remove(c_name + "/collection.json")
    print(f"Testing check on (broken) {c_name}")
    if not (dataset.check(c_name) == False):
        err = dataset.error_message()
        t.error(f"Failed, (after break) expected check False got True for {c_name} (err: {err})")
    else:
        t.print(f"Should have see error output for broken {c_name}")

    # Repair our collection
    t.print("Testing repair on", c_name)
    if dataset.repair(c_name) == False:
        err = dataset.error_message()
        t.error("Failed, expected repair to return True, got, ", err)
    if os.path.exists(os.path.join(c_name,  "collection.json")) == False:
        t.error(f"Failed, expected recreated {c_name}/collection.json")
 
        
def test_attachments(t, c_name):
    t.print("Testing attach, attachments, detach and prune")
    # Generate two files to attach.
    filenames = ['a1.txt', 'a2.txt']
    for i, f_name in enumerate(filenames):
        with open(f_name, 'w') as text_file:
            text_file.write(f'This is file {f_name} ({i})' + "\n")

    if dataset.status(c_name) == False:
        t.error("Failed,", c_name, "missing")
        return
    keys = dataset.keys(c_name)
    if len(keys) < 1:
        t.error("Failed,", c_name, "should have keys")
        return

    print(f'DEBUG len(keys) -> {len(keys)}')
    key = keys[0]
    print(f'DEBUG key -> {key}, attaching {filenames}')
    if dataset.attach(c_name, key, filenames) == False:
        err = dataset.error_message()
        t.error(f"Failed to attach files for {c_name} -> {key} => {filenames} : {err}")
        return

    l = dataset.attachments(c_name, key)
    if len(l) != 2:
        t.error(f"Failed, expected two attachments for {c_name} -> {key} got ({len(l)}) {l}")
        return

    #Check that attachments should not be impacted by update
    if dataset.update(c_name, key, {"key": key, "testing":"update"}) == False:
        err = dataset.error_message()
        t.error("Failed, to update record", c_name, key, err)
        return
    l = dataset.attachments(c_name, key)
    if len(l) != 2:
        t.error("Failed, expected two attachments after update for", c_name, key, "got", l)
        return

    if os.path.exists(filenames[0]):
        os.remove(filenames[0])
    if os.path.exists(filenames[1]):
        os.remove(filenames[1])

    # First try detaching one file.
    if dataset.detach(c_name, key, [filenames[1]]) == False:
        err = dataset.error_message()
        t.error("Failed, expected True for", c_name, key, filenames[1], ', ', err)
    if os.path.exists(filenames[1]):
        os.remove(filenames[1])
    else:
        t.error("Failed to detch", filenames[1], "from", c_name, key)

    # Test explicit filenames detch
    if dataset.detach(c_name, key, filenames) == False:
        err = dataset.error_message()
        t.error("Failed, expected True for", c_name, key, filenames, ', ', err)

    for fname in filenames:
        if os.path.exists(fname):
            os.remove(fname)
        else:
            t.error("Failed, expected", fname, "to be detached from", c_name, key)

    # Test detaching all files
    if dataset.detach(c_name, key, []) == False:
        err = dataset.error_message()
        t.error("Failed, expected True for (detaching all)", c_name, key, ', ', err)
    for fname in filenames:
        if os.path.exists(fname):
            os.remove(fname)
        else:
            t.error("Failed, expected", fname, "for detaching all from", c_name, key)

    if dataset.prune(c_name, key, [filenames[0]]) == False:
        err = dataset.error_messag()
        t.error("Failed, expected True for prune", c_name, key, [filenames[0]], ', ', err)
    l = dataset.attachments(c_name, key)
    if len(l) != 1:
        t.error("Failed, expected one file after prune for", c_name, key, [filenames[0]], "got", l)

    if dataset.prune(c_name, key, []) == False:
        err = dataset.error_message()
        t.error("Failed, expected True for prune (all)", c_name, key, ', ', err)
    l = dataset.attachments(c_name, key)
    if len(l) != 0:
        t.error("Failed, expected zero files after prune for", c_name, key, "got", l)

    
def test_join(t, c_name):
    key = "test_join1"
    obj1 = { "id": key, "one": 1}
    obj2 = { "id": key, "two": 2}
    if dataset.status(c_name) == False:
        t.error("Failed, collection status is False,", c_name)
        return
    ok = dataset.has_key(c_name, key)
    err = ''
    if ok == True:
        ok = dataset.update(collection_nane, key, obj1)
    else:
        ok = dataset.create(c_name, key, obj1)
    if ok == False:
        err = dataset.error_message()
        t.error(f'Failed, could not add record for test ({c_name}, {key}, {obj1}), {err}')
        return
    if dataset.join(c_name, key, obj2, overwrite = False) == False:
        err = dataset.error_message()
        t.error(f'Failed, join for {c_name}, {key}, {obj2}, overwrite = False -> {err}')
    obj_result, err = dataset.read(c_name, key)
    if err != '':
        t.error(f'Unexpected error for {key} in {c_name}, {err}')
    if obj_result.get('one') != 1:
        t.error(f'Failed to join append key {key}, {obj_result}')
    if obj_result.get("two") != 2:
        t.error(f'Failed to join append key {key}, {obj_result}')
    obj2['one'] = 3
    obj2['two'] = 3
    obj2['three'] = 3
    if dataset.join(c_name, key, obj2, overwrite = True) == False:
        err = dataset.error_message()
        t.error(f'Failed to join overwrite {c_name}, {key}, {obj2}, overwrite = True -> {err}')
    obj_result, err = dataset.read(c_name, key)
    if err != '':
        t.error(f'Unexpected error for {key} in {c_name}, {err}')
    for k in obj_result:
        if k != 'id' and obj_result[k] != 3:
            t.error('Failed to update value in join overwrite', k, obj_result)
    
#
# test_issue43() When exporting records to a table using
# use_srict_dotpath(True), the rows are getting miss aligned.
#
def test_issue43(t, c_name, csv_name):
    if os.path.exists(c_name):
        shutil.rmtree(c_name)
    if os.path.exists(csv_name):
        os.remove(csv_name)
    if dataset.init(c_name, "") == False:
        err = dataset.error_message()
        t.error(f'Failed, need a {c_name} to run test, {err}')
        return
    table = {
            "r1": {
                "c1": "one",
                "c2": "two",
                "c3": "three",
                "c4": "four"
                },
            "r2": {
                "c1": "one",
                "c3": "three",
                "c4": "four"
                },

            "r3": {
                "c1": "one",
                "c2": "two",
                "c4": "four"
                },
            "r4": {
                "c1": "one",
                "c2": "two",
                "c3": "three"
                },
            "r5": {
                "c1": "one",
                "c2": "two",
                "c3": "three",
                "c4": "four"
                }
            }
    for key in table:
        row = table[key]
        row['key'] = key # Save the key/id along with the row data
        if dataset.create(c_name, key, row) == False:
            err = dataset.error_message()
            t.error(f"Can't add test row {key} to {c_name}, {err}")
            return

    dataset.use_strict_dotpath(False)
    # Setup frame
    frame_name = 'f1'
    keys = dataset.keys(c_name)
    if dataset.frame_create(c_name, frame_name, keys, 
        [".key",".c1",".c2",".c3",".c4"], ["key", "c1", "c2", "c3", "c4"]) == False:
        err = dataset.error_message()
        t.error(err)
        return
    if dataset.export_csv(c_name, frame_name, csv_name) == False:
       err = dataset.error_message()
       t.error(f'export_csv({c_name}, {frame_name}, {csv_name} should have emitted warnings, not error, {err}')
       return
    with open(csv_name, mode = 'r', encoding = 'utf-8') as f:
        rows = f.read()

    for row in rows.split('\n'):
        if len(row) > 0:
            cells = row.split(',')
            if len(cells) < 5:
                t.error(f'row error {csv_name} for {cells}')


def test_clone_sample(t, c_name, sample_size, training_name, training_dsn, test_name, test_dsn):
    if os.path.exists(training_name):
        shutil.rmtree(training_name)
    if os.path.exists(test_name):
        shutil.rmtree(test_name)
    if dataset.clone_sample(c_name, training_name, training_dsn, test_name, test_dsn, sample_size) == False:
        err = dataset.error_message()
        t.error(f"can't clone sample {c_name} size {sample_size} into {training_name}, {test_name} error {err}")

def test_frame(t, c_name):
    if os.path.exists(c_name):
        shutil.rmtree(c_name)
    if dataset.init(c_name, "") == False:
        err = dataset.error_message()
        t.error(err)
        return
    data = [
        { "id":    "A", "one":   "one", "two":   22, "three": 3.0, "four":  ["one", "two", "three"] },
        { "id":    "B", "two":   2000, "three": 3000.1 },
        { "id": "C" },
        { "id":    "D", "one":   "ONE", "two":   20, "three": 334.1, "four":  [] }
    ]
    keys = []
    dot_paths = [".id", ".one", ".two", ".three", ".four"]
    labels = ["id", "one", "two", "three", "four"]
    for row in data:
        key = row['id']
        keys.append(key)
        dataset.create(c_name, key, row)
    f_name = 'f1'
    if dataset.frame_create(c_name, f_name, keys, dot_paths, labels) == False:
        err = dataset.error_message()
        t.error(err)
    if dataset.frame_reframe(c_name, f_name) == False:
        err = dataset.error_message()
        t.error(err)
    l = dataset.frame_names(c_name)
    if len(l) != 1 or l[0] != 'f1':
        t.error(f"expected one frame name, f1, got {l}")
    if dataset.delete_frame(c_name, f_name) == False:
        err = dataset.error_message()
        t.error(f'delete_frame({c_name}, {f_name}), {err}')

def test_frame_objects(t, c_name):
    if dataset.status(c_name) == True:
        dataset.close(c_name)
        if os.path.exists(c_name):
            shutil.rmtree(c_name)
    if dataset.init(c_name, "") == False:
        err = dataset.error_message()
        t.error(f'init({c_name}), {err}')
        return
    data = [
        { "id":    "A", "nameIdentifiers": [
                {
                    "nameIdentifier": "0000-000X-XXXX-XXXX",
                    "nameIdentifierScheme": "ORCID",
                    "schemeURI": "http://orcid.org/"
                },
                {
                    "nameIdentifier": "H-XXXX-XXXX",
                    "nameIdentifierScheme": "ResearcherID",
                    "schemeURI": "http://www.researcherid.com/rid/"
                }], "two":   22, "three": 3.0, "four":  ["one", "two", "three"] },
        { "id":    "B", "two":   2000, "three": 3000.1 },
        { "id": "C" },
        { "id":    "D", "nameIdentifiers": [
                {
                    "nameIdentifier": "0000-000X-XXXX-XXXX",
                    "nameIdentifierScheme": "ORCID",
                    "schemeURI": "http://orcid.org/"
                }], "two":   20, "three": 334.1, "four":  [] }
    ]
    keys = []
    dot_paths = [".id",".nameIdentifiers",".nameIdentifiers[:].nameIdentifier",".two", ".three", ".four"]
    labels = ["id","nameIdentifiers", "nameIdentifier", "two", "three", "four"]
    for row in data:
        key = row['id']
        keys.append(key)
        err = dataset.create(c_name, key, row)
    f_name = 'f1'
    if dataset.frame_create(c_name, f_name, keys, dot_paths, labels) == False:
        err = dataset.error_message()
        t.error(f'frame_create({c_name}, {f_name}, {keys}, {dot_paths}, {labels}), {err}')
        return
    f_keys = dataset.frame_keys(c_name, f_name)
    if len(f_keys) != len(keys):
        t.error(f'expected {len(keys)}, got {len(f_keys)}')
    if dataset.frame_refresh(c_name, f_name) == False:
        err = dataset.error_message()
        t.error(f'frame_reframe({c_name}, {f_name}), {err}')
    l = dataset.frame_names(c_name)
    if len(l) != 1 or l[0] != 'f1':
        t.error(f"expected one frame name, f1, got {l}")
    object_result = dataset.frame_objects(c_name, f_name)
    if len(object_result) != 4:
        t.error(f'Did not get correct number of objects back, expected 4 got {len(object_result)}, {object_result}')
    count_nameId = 0
    count_nameIdObj = 0
    for obj in object_result:
        if 'id' not in obj:
            t.error('Did not get id in object')
        if 'nameIdentifiers' in obj:
            count_nameId += 1
            for idv in obj['nameIdentifiers']:
                if 'nameIdentifier' not in idv:
                    t.error('Missing part of object')
        if 'nameIdentifier' in obj:
            count_nameIdObj += 1
            if "0000-000X-XXXX-XXXX" not in obj['nameIdentifier']:
                t.error('Missing object in complex dot path')
    if count_nameId != 2:
        t.error(f"Incorrect number of nameIdentifiers elements, expected 2, got {count_nameId}")
    if count_nameIdObj != 2:
        t.error(f"Incorrect number of nameIdentifier elements, expected 2, got {count_nameIdObj}")
    if dataset.delete_frame(c_name, f_name) == False:
        err = dataset.error_message()
        t.error(f'delete_frame({c_name}, {f_name}), {err}')

#
# test_sync_csv (issue 80) - add tests for sync_send_csv, sync_recieve_csv
#
def test_sync_csv(t, c_name):
    # Setup test collection
    if os.path.exists(c_name):
        shutil.rmtree(c_name)
    if dataset.init(c_name, "") == False:
        err = dataset.error_message()
        t.error(f'init({c_name}) failed, {err}')
        return

    # Setup test CSV instance
    t_data = [
            { "key": "one", "value": 1 },
            { "key": "two", "value": 2 },
            { "key": "three", "value": 3  }
    ]
    csv_name = c_name.strip(".ds") + ".csv"
    if os.path.exists(csv_name):
        os.remove(csv_name)
    with open(csv_name, 'w') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames = ["key", "value" ])
        csv_writer.writeheader()
        for obj in t_data:
            csv_writer.writerow(obj)
        
    # Import CSV into collection
    if dataset.import_csv(c_name, csv_name, True) == False:
        err = dataset.error_message()
        t.error(f'import_csv({c_name}, {csv_name}, True) failed, {err}')
        return
    for key in [ "one", "two", "three" ]:
        if dataset.has_key(c_name, key) == False:
            t.error(f"expected has_key({key}) == True, got False")
    if dataset.has_key(c_name, "five") == True:
        t.error(f"expected has_key('five') == False, got True")
    if dataset.create(c_name, "five", {"key": "five", "value": 5}) == False:
        err = dataset.error_message()
        t.error(f'create({c_name}, "five", {"value": 5}) failed, {err}')
        return

    # Setup frame
    frame_name = 'test_sync'
    keys = dataset.keys(c_name)
    if dataset.frame_create(c_name, frame_name, keys, [".key", ".value"], ["key", "value"] ) == False:
        err = dataset.error_message()
        t.error(f'frame_create({c_name}, {frame_name}, ...) failed, {err}')
        return

    #NOTE: Tests for sync_send_csv and sync_receive_csv
    if dataset.sync_send_csv(c_name, frame_name, csv_name) == False:
        err = dataset.error_message()
        t.error(f'sync_send_csv({c_name}, {frame_name}, {csv_name}) failed, {err}')
        return
    with open(csv_name) as fp:
        src = fp.read()
        if 'five' not in src:
            t.error(f"expected 'five' in src, got {src}")

    # Now remove "five" from collection
    if dataset.delete(c_name, "five") == False:
        err = dataset.error_message()
        t.error(f'delete({c_name}, "five") failed, {err}')
        return
    if dataset.has_key(c_name, "five") == True:
        t.error(f"expected has_key(five) == False, got True")
        return
    if dataset.sync_recieve_csv(c_name, frame_name, csv_name, False) == False:
        err = dataset.error_message()
        t.error(f'sync_receive_csv({c_name}, {frame_name}, {csv_name}) failed, {err}')
        return
    if dataset.has_key(c_name, "five") == False:
        t.error(f"expected has_key(five) == True, got False")
        return


#
# Test harness
#
class ATest:
    def __init__(self, test_name, verbose = False):
        self._test_name = test_name
        self._error_count = 0
        self._verbose = False

    def test_name(self):
        return self._test_name

    def is_verbose(self):
        return self._verbose

    def verbose_on(self):
        self._verbose = True

    def verbose_off(self):
        self.verbose = False

    def print(self, *msg):
        if self._verbose == True:
            print(*msg)

    def error(self, *msg):
        fn_name = self._test_name
        self._error_count += 1
        print(f"\t{fn_name}", *msg)

    def error_count(self):
        return self._error_count

class TestRunner:
    def __init__(self, set_name, verbose = False):
        self._set_name = set_name
        self._tests = []
        self._error_count = 0
        self._verbose = verbose

    def add(self, fn, params = []):
        self._tests.append((fn, params))

    def run(self):
        for test in self._tests:
            fn_name = test[0].__name__
            t = ATest(fn_name, self._verbose)
            fn, params = test[0], test[1]
            fn(t, *params)
            error_count = t.error_count()
            if error_count > 0:
                print(f"\t\t{fn_name} failed, {error_count} errors found")
                if fail_fast == True:
                    return
            else:
                print(f"\t\t{fn_name} OK")
            self._error_count += error_count
        error_count = self._error_count
        set_name = self._set_name
        if error_count > 0:
            print(f"Failed {set_name}, {error_count} total errors found")
            sys.exit(1)
        print("PASS")
        print("Ok", __file__)
        sys.exit(0)

#
# Main processing
#
if __name__ == "__main__":
    print("Starting dataset_test.py")
    print("Testing dataset version", dataset.dataset_version())

    # Pre-test check
    error_count = 0
    ok = True
    dataset.verbose_off()

    c_name = "test_collection.ds"
    test_runner = TestRunner(os.path.basename(__file__))
    test_runner.add(test_setup, [c_name])
    test_runner.add(test_basic, [c_name])
    test_runner.add(test_keys, [c_name])
    test_runner.add(test_issue32, [c_name])
    test_runner.add(test_attachments, [c_name])
    test_runner.add(test_join, [c_name])
    test_runner.add(test_issue43,["test_issue43.ds", "test_issue43.csv"])
    # NOTE: simple cloning requires a DSN for training and test datasets
    test_runner.add(test_clone_sample, ["test_collection.ds", 5, "test_training.ds", "", "test_test.ds", ""])
    test_runner.add(test_frame, ["test_frame.ds"])
    test_runner.add(test_frame_objects, ["test_frame.ds"])
    test_runner.add(test_sync_csv, ["test_sync_csv.ds"])
    test_runner.add(test_check_repair, ["test_check_and_repair.ds"])
    test_runner.add(test_issue12, ['test_issue12.ds'])

    test_runner.run()

