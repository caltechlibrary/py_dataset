/* Code generated by cmd/cgo; DO NOT EDIT. */

/* package command-line-arguments */


#line 1 "cgo-builtin-export-prolog"

#include <stddef.h>

#ifndef GO_CGO_EXPORT_PROLOGUE_H
#define GO_CGO_EXPORT_PROLOGUE_H

#ifndef GO_CGO_GOSTRING_TYPEDEF
typedef struct { const char *p; ptrdiff_t n; } _GoString_;
#endif

#endif

/* Start of preamble from import "C" comments.  */




/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */
#line 1 "cgo-gcc-export-header-prolog"

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt64 GoInt;
typedef GoUint64 GoUint;
typedef size_t GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
#ifdef _MSC_VER
#include <complex.h>
typedef _Fcomplex GoComplex64;
typedef _Dcomplex GoComplex128;
#else
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;
#endif

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_64_bit_pointer_matching_GoInt[sizeof(void*)==64/8 ? 1:-1];

#ifndef GO_CGO_GOSTRING_TYPEDEF
typedef _GoString_ GoString;
#endif
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif


// error_clear will set the global error state to nil.
//
extern void error_clear();

// error_message returns an error message previously recorded or
// an empty string if no errors recorded
//
extern char* error_message();

// use_strict_dotpath sets the library option value for
// enforcing strict dotpaths. 1 is true, any other value is false.
//
extern int use_strict_dotpath(int v);

// is_verbose returns the library options' verbose value.
//
extern int is_verbose();

// verbose_on set library verbose to true
//
extern void verbose_on();

// verbose_off set library verbose to false
//
extern void verbose_off();

// dataset_version returns the version of libdataset.
//
extern char* dataset_version();

// init_collection intializes a collection and records as much metadata
// as it can from the execution environment (e.g. username,
// datetime created). NOTE: New parameter required, storageType. This
// can be either "pairtree" or "sqlstore".
//
extern int init_collection(char* name, char* cStorageType);

// is_collection_open returns true (i.e. one) if a collection has been opened by libdataset, false (i.e. zero) otherwise
//
extern int is_collection_open(char* cName);

// open_collection returns 0 on successfully opening a collection 1 otherwise. Sets error messages if needed.
//
extern int open_collection(char* cName);

// collections returns a JSON list of collection names that are open otherwise an empty list.
//
extern char* collections();

// close_collection closes a collection previously opened.
//
extern int close_collection(char* cName);

// close_all_collections closes all collections previously opened
//
extern int close_all_collections();

// collection_exits checks to see if a collection exists or not.
//
extern int collection_exists(char* cName);

// check_collection runs the analyzer over a collection and looks for
// problem records.
//
extern int check_collection(char* cName);

// repair_collection runs the analyzer over a collection and repairs JSON
// objects and attachment discovered having a problem. Also is
// useful for upgrading a collection between dataset releases.
//
extern int repair_collection(char* cName);

// clone_collection takes a collection name, a JSON array of keys and creates
// a new collection with a new name based on the origin's collections'
// objects. NOTE: If you are using pairtree dsn can be an empty string
// otherwise it needs to be a dsn to connect to the SQL store.
//
extern int clone_collection(char* cName, char* cDsn, char* cKeys, char* dName);

// clone_sample is like clone both generates a sample or test and
// training set of sampled of the cloned collection. NOTE: The
// training name and testing name are followed by their own dsn values.
// If the dsn is an empty string then a pairtree store is assumed.
//
extern int clone_sample(char* cName, char* cTrainingName, char* cTrainingDsn, char* cTestName, char* cTestDsn, int cSampleSize);

// import_csv - import a CSV file into a collection
// syntax: COLLECTION CSV_FILENAME ID_COL
//
// options that should support sensible defaults:
//
//	cUseHeaderRow
//	cOverwrite
//
extern int import_csv(char* cName, char* cCSVFName, int cIDCol, int cUseHeaderRow, int cOverwrite);

// export_csv - export collection objects to a CSV file
// syntax: COLLECTION FRAME CSV_FILENAME
//
extern int export_csv(char* cName, char* cFrameName, char* cCSVFName);

// sync_send_csv - synchronize a frame sending data to a CSV file
// returns 1 (True) on success, 0 (False) otherwise.
//
extern int sync_send_csv(char* cName, char* cFName, char* cCSVFilename, int cSyncOverwrite);

// sync_recieve_csv - synchronize a frame recieving data from a CSV file
// returns 1 (True) on success, 0 (False) otherwise.
//
extern int sync_recieve_csv(char* cName, char* cFName, char* cCSVFilename, int cSyncOverwrite);

// has_key returns 1 if the key exists in collection or 0 if not.
//
extern int has_key(char* cName, char* cKey);

// keys returns JSON source of an array of keys from the collection
//
extern char* keys(char* cName);

// create_object takes JSON source and adds it to the collection with
// the provided key.
//
extern int create_object(char* cName, char* cKey, char* cSrc);

// read_object takes a key and returns JSON source of the record
//
extern char* read_object(char* cName, char* cKey, int cCleanObject);

// THIS IS AN UGLY HACK, Python ctypes doesn't **easily** support
// undemensioned arrays of strings. So we will assume the array of
// keys has already been transformed into JSON before calling
// read_list.
//
extern char* read_object_list(char* cName, char* cKeysAsJSON, int cCleanObject);

// update_object takes a key and JSON source and replaces the record
// in the collection.
//
extern int update_object(char* cName, char* cKey, char* cSrc);

// delete_object takes a key and removes a record from the collection
//
extern int delete_object(char* cName, char* cKey);

// join_objects takes a collection name, a key, and merges JSON source with an
// existing JSON record. If overwrite is 1 it overwrites and replaces
// common values, if not 1 it only adds missing attributes.
//
extern int join_objects(char* cName, char* cKey, char* cObjSrc, int cOverwrite);

// count_objects returns the number of objects (records) in a collection.
// if an error is encounter a -1 is returned.
//
extern int count_objects(char* cName);

// object_path returns the path on disc to an JSON object document
// in the collection.
//
extern char* object_path(char* cName, char* cKey);

// create_objects - is a function to creates empty a objects in batch.
// It requires a JSON list of keys to create. For each key present
// an attempt is made to create a new empty object based on the JSON
// provided (e.g. `{}`, `{"is_empty": true}`). The reason to do this
// is that it means the collection.json file is updated once for the
// whole call and that the keys are now reserved to be updated separately.
// Returns 1 on success, 0 if errors encountered.
//
extern int create_objects(char* cName, char* keysAsJSON, char* objectAsJSON);

// update_objects - is a function to update objects in batch.
// It requires a JSON array of keys and a JSON array of
// matching objects. The list of keys and objects are processed
// together with calls to update individual records. Returns 1 on
// success, 0 on error.
//
extern int update_objects(char* cName, char* keysAsJSON, char* objectsAsJSON);

// list_objects returns JSON array of objects in a collections based on a
// JSON array of keys.
//
extern char* list_objects(char* cName, char* cKeys);

// attach will attach a file to a JSON object in a collection. It takes
// a semver string (e.g. v0.0.1) and associates that with where it stores
// the file.  If semver is v0.0.0 it is considered unversioned, if v0.0.1
// or larger it is considered versioned.
//
extern int attach(char* cName, char* cKey, char* cSemver, char* cFNames);

// attachments returns a list of attachments and their size in
// associated with a JSON obejct in the collection.
//
extern char* attachments(char* cName, char* cKey);

// detach exports the file associated with the semver from the JSON
// object in the collection. The file remains "attached".
//
extern int detach(char* cName, char* cKey, char* cSemver, char* cFNames);

// prune removes an attachment by semver from a JSON object in the
// collection. This is destructive, the file is removed from disc.
//
extern int prune(char* cName, char* cKey, char* cSemver, char* cFNames);

// frame retrieves a frame including its metadata. NOTE:
// if you just want the object list, use frame_objects().
//
extern char* frame(char* cName, char* cFName);

// has_frame returns 1 (true) if frame name exists in collection, 0 (false) otherwise
//
extern int has_frame(char* cName, char* cFName);

// frame_keys takes a collection name and frame name and returns a list of keys from the frame or an empty list.
// The list is expressed as a JSON source.
//
extern char* frame_keys(char* cName, char* cFName);

// frame_create defines a new frame an populates it.
//
extern int frame_create(char* cName, char* cFName, char* cKeysSrc, char* cDotPathsSrc, char* cLabelsSrc);

// frame_objects retrieves a JSON source list of objects from a frame.
//
extern char* frame_objects(char* cName, char* cFName);

// frame_refresh refresh the contents of the frame using the
// existing keys associated with the frame and the current state
// of the collection.  NOTE: If a key is missing
// in the collection then the key and object is removed.
//
extern int frame_refresh(char* cName, char* cFName);

// frame_reframe will change the key and object list in a frame based on
// the key list provided and the current state of the collection.
//
extern int frame_reframe(char* cName, char* cFName, char* cKeysSrc);

// frame_clear will clear the object list and keys associated with a frame.
//
extern int frame_clear(char* cName, char* cFName);

// frame_delete will removes a frame from a collection
//
extern int frame_delete(char* cName, char* cFName);

// frame_names returns a JSON array of frames names in the collection.
//
extern char* frame_names(char* cName);

// frame_grid takes a frames object list and returns a grid
// (2D JSON array) representation of the object list.
// If the "header row" value is 1 a header row of labels is
// included, otherwise it is only the values of returned in the grid.
//
extern char* frame_grid(char* cName, char* cFName, int cIncludeHeaderRow);

// get_version will rerturn the dataset "version" used to create/manage the collection. If want a version associated with the collection itself see the codemeta.json file in the root folder of the collection.
//
extern char* get_version(char* cName);

#ifdef __cplusplus
}
#endif
