/* Code generated by cmd/cgo; DO NOT EDIT. */

/* package command-line-arguments */


#line 1 "cgo-builtin-export-prolog"

#include <stddef.h> /* for ptrdiff_t below */

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
typedef __SIZE_TYPE__ GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;

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

extern void error_clear();

extern char* error_message();

extern int use_strict_dotpath(int p0);

extern int is_verbose();

extern void verbose_on();

extern void verbose_off();

extern char* dataset_version();

extern int init_collection(char* p0, int p1);

extern int has_key(char* p0, char* p1);

extern int create_record(char* p0, char* p1, char* p2);

extern char* read_record(char* p0, char* p1);

extern int update_record(char* p0, char* p1, char* p2);

extern int delete_record(char* p0, char* p1);

extern int join(char* p0, char* p1, char* p2, int p3);

extern char* keys(char* p0, char* p1, char* p2);

extern char* key_filter(char* p0, char* p1, char* p2);

extern char* key_sort(char* p0, char* p1, char* p2);

extern int count(char* p0);

extern int indexer(char* p0, char* p1, char* p2, char* p3, int p4);

extern int deindexer(char* p0, char* p1, char* p2, int p3);

extern char* find(char* p0, char* p1, char* p2);

// import_csv - import a CSV file into a collection
// syntax: COLLECTION CSV_FILENAME ID_COL
//
// options that should support sensible defaults:
//
//     cUseHeaderRow
//     cOverwrite
//

extern int import_csv(char* p0, char* p1, int p2, int p3, int p4);

// export_csv - export collection objects to a CSV file
// syntax: COLLECTION FRAME CSV_FILENAME
//

extern int export_csv(char* p0, char* p1, char* p2);

// import_gsheet - import a GSheet into a collection
// syntax: COLLECTION GSHEET_ID SHEET_NAME ID_COL CELL_RANGE
//
// options that should support sensible defaults:
//
//    cUseHeaderRow
//    cOverwrite
//

extern int import_gsheet(char* p0, char* p1, char* p2, int p3, char* p4, int p5, int p6);

// export_gsheet - export collection objects to a GSheet
// syntax: COLLECTION FRAME GSHEET_ID GSHEET_NAME CELL_RANGE
//

extern int export_gsheet(char* p0, char* p1, char* p2, char* p3, char* p4);

extern int status(char* p0);

extern char* list(char* p0, char* p1);

extern char* path(char* p0, char* p1);

extern int check(char* p0);

extern int repair(char* p0);

extern int attach(char* p0, char* p1, char* p2);

extern char* attachments(char* p0, char* p1);

extern int detach(char* p0, char* p1, char* p2);

extern int prune(char* p0, char* p1, char* p2);

extern int clone(char* p0, char* p1, char* p2);

extern int clone_sample(char* p0, char* p1, char* p2, int p3);

extern char* grid(char* p0, char* p1, char* p2);

extern char* frame(char* p0, char* p1, char* p2, char* p3);

extern int has_frame(char* p0, char* p1);

extern char* frames(char* p0);

extern int reframe(char* p0, char* p1, char* p2);

extern int frame_labels(char* p0, char* p1, char* p2);

extern int delete_frame(char* p0, char* p1);

// sync_send_csv - synchronize a frame sending data to a CSV file
//

extern int sync_send_csv(char* p0, char* p1, char* p2, int p3);

// sync_recieve_csv - synchronize a frame recieving data from a CSV file
//

extern int sync_recieve_csv(char* p0, char* p1, char* p2, int p3);

// sync_send - synchronize a frame sending data to a GSheet
//

extern int sync_send_gsheet(char* p0, char* p1, char* p2, char* p3, char* p4, int p5);

// sync_recieve_gsheet - synchronize a frame recieving data from a GSheet
//

extern int sync_recieve_gsheet(char* p0, char* p1, char* p2, char* p3, char* p4, int p5);

#ifdef __cplusplus
}
#endif