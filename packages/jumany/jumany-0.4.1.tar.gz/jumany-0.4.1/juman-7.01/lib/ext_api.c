#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "juman.h"
#include "ext_api.h"

typedef struct ext_t {
	char * in_buf;
	size_t in_buf_size;
	char * word_buf;
	size_t word_buf_size;
	EXT_MRPH_T * mrphs_buf;
	int max_mrphs;
	int pos;
} EXT_T;

//	Store in global
EXT_T Dext;
char * NullStr = "";

extern FILE * Jumanrc_Fileptr;
extern BOOL set_jumanrc_fileptr_min(const char *option_rcfile);
extern BOOL	juman_init_rc(FILE *fp);
extern void juman_init_etc(void);
extern int	juman_close(void);
extern int juman_sent(void);
extern MRPH *prepare_path_mrph(int path_num , int para_flag);
extern void set_encoding_opt(const char * s_encoding);

extern int p_buffer_num;
extern PROCESS_BUFFER * p_buffer;
extern int * path_buffer;
extern U_CHAR midasi1[MIDASI_MAX];
extern U_CHAR midasi2[MIDASI_MAX];
extern U_CHAR yomi[MIDASI_MAX];
extern CLASS		Class[CLASSIFY_NO + 1][CLASSIFY_NO + 1];
extern TYPE		Type[TYPE_NO];
extern FORM		Form[TYPE_NO][FORM_NO];

static char * wordcopy(char **pword_pos, size_t *pword_buf_rest, const char * word);

#define free(buff) { \
	if( (buff)==NULL) free((buff)); \
	(buff) = NULL; \
}

///	Set encoding
///	It must be called before ext_init.
///	If specified wrong encoding name, error will occure in ext_init.
/// @param s_encoding Comma separated string of input and output encoding.
///	If comma does not exist, both input and output encoding considered this value.
///	If NULL or null string, considered same as inner encoding and will not do encoding.
void ext_set_encoding(const char *s_encoding) {
	set_encoding_opt(s_encoding);
}
	
///	Initialize lib
///	@param s_rcfile	Path to jumanrc
///	@param word_buf_size Word buffer size. It is copied midasi1, yomi, and midasi2.
///	@param max_mrphs Morpheme buffer size in number. 
///	@return 
///	- EXT_SUCCESS:	Success 
///	- EXT_RC_ERROR:	Resource file error.
///	- EXT_MALLOC_ERROR:	Cannot allocate memory.
EXT_RES_CODE ext_init(const char *s_rcfile, size_t word_buf_size, int max_mrphs) {
	if(FALSE==set_jumanrc_fileptr_min(s_rcfile))	return EXT_FILE_NOT_EXISTS;
	if(FALSE==juman_init_rc(Jumanrc_Fileptr)) return EXT_RC_ERROR;
    juman_init_etc();
#ifdef HAVE_REGEX_H
	Unkword_Pat_Num = compile_unkword_patterns();
#endif
	Dext.in_buf = get_input_buff(&(Dext.in_buf_size));
	Dext.word_buf_size = word_buf_size? word_buf_size: LENMAX;
	Dext.max_mrphs = max_mrphs? max_mrphs: DEF_MAX_ITEMS;
	Dext.word_buf = malloc(Dext.word_buf_size);
	Dext.mrphs_buf = malloc(sizeof(EXT_MRPH_T) * Dext.max_mrphs);
	if(NULL==Dext.word_buf || NULL==Dext.mrphs_buf) {
		free(Dext.word_buf);
		free(Dext.mrphs_buf);
		return EXT_MALLOC_ERROR;
	}
	Dext.pos = -1;
	return EXT_SUCCESS;
}

///	Close extlib
void ext_close() {
	free(Dext.word_buf);
	free(Dext.mrphs_buf);
	juman_close();
}
	
///	Get input buffer to write.
///	@param psize [out]Buffer size.
///	@return Buffer address.
char * ext_get_input_buff(size_t *psize) {
	*psize = Dext.in_buf_size;
	return Dext.in_buf;
}

///	Get morpheme buffer to read.
///	@return Buffer address.
EXT_MRPH_T * ext_get_mrph_buff() {
	return Dext.mrphs_buf;
}

///	Analyze with best path
///	@return 
///	- EXT_SUCCESS:	Success 
///	- EXT_ERROR:	Error
EXT_RES_CODE ext_analyze() {
    int i, j, last;
    MRPH *mrph_p,*mrph_p1;

	if(FALSE==juman_sent()) return EXT_ANA_ERROR;
	//	from print_best_path
    j = 0;
    last = p_buffer_num-1;
    do {
		last = p_buffer[last].path[0];
		path_buffer[j] = last;
		j++;
	} while ( p_buffer[last].path[0] );
	Dext.pos = i=j-1;
	return EXT_SUCCESS;
}

///	Get result in mopheme buffer
///	@param pnum_mrphs [out]Number of mopheme in buffer
///	@return 
///	- EXT_SUCCESS:	Put all morpheme.
///	- EXT_WORD_BUFF_OVER:	Word buffer is not enough. Call more to get all morpheme.
///	- EXT_MRPH_BUFF_OVER:	Morpheme buffer is not enough. Call more to get all morpheme.
EXT_RES_CODE ext_get_result(int *pnum_mrphs) {
	
	char * word_pos;
	size_t word_buf_rest;
	int path_num;
	MRPH *mrph_p;
	EXT_MRPH_T *pitem;
	
	word_pos = Dext.word_buf;
	word_buf_rest = Dext.word_buf_size;
	word_pos[word_buf_rest-1] = 0;
	*pnum_mrphs = 0;

	while(Dext.pos>=0 && *pnum_mrphs < Dext.max_mrphs) {
		path_num = path_buffer[Dext.pos];
		if ((mrph_p = prepare_path_mrph(path_num, 0)) == NULL) continue;
		pitem = Dext.mrphs_buf + *pnum_mrphs;
		pitem->midasi1 = wordcopy(&word_pos, &word_buf_rest, midasi1);
		if(NULL==pitem->midasi1) return EXT_WORD_BUFF_OVER;
		pitem->yomi = wordcopy(&word_pos, &word_buf_rest, yomi);
		if(NULL==pitem->yomi) return EXT_WORD_BUFF_OVER;
		pitem->midasi2 = wordcopy(&word_pos, &word_buf_rest, midasi2);
		if(NULL==pitem->midasi2) return EXT_WORD_BUFF_OVER;
		pitem->hinsi = mrph_p->hinsi;
		pitem->bunrui = mrph_p->bunrui;
		pitem->katuyou1 = mrph_p->katuyou1;
		pitem->katuyou2 = mrph_p->katuyou2;

		(*pnum_mrphs)++;
		Dext.pos--;
	}
	if(Dext.pos>=0) return EXT_MRPH_BUFF_OVER;
	return EXT_SUCCESS;
}

static char * wordcopy(char **pword_pos, size_t *pword_buf_rest, const char * word) {
	char * pwritten;
	int len;
	len = strlen(word);
	if(len+1 >= *pword_buf_rest) return NULL;
	pwritten = strcpy(*pword_pos, word);
	(*pword_buf_rest) -= len+1;
	(*pword_pos) += len+1;
	return pwritten;
}

///	Get hinsi string.
///	@param hinsi Index of hinsi.
///	@return String of bunrui. if index is wrong, return null string.
const char * ext_get_hinsi(int hinsi) {
	return (Class[hinsi][0].id==NULL)? 
		NullStr: (const char *)Class[hinsi][0].id;
}

///	Get all hinsi
///	@param list [out]List of hinsi. It ranges from 1 to return num-1.
///	@return Nunber of list items.
int ext_get_all_hinsi(const char ** list) {
	int i;
	*list++ = NullStr;
	for (i=1 ; Class[i][0].id!=NULL && i<=CLASSIFY_NO; i++) {
		*list++ = Class[i][0].id;
	}
	return i;
}

///	Get bunrui string.
///	@param hinsi Index of hinsi.
///	@param bunrui Index of bunrui.
///	@return String of bunrui. if index is wrong, return null string.
const char * ext_get_bunrui(int hinsi, int bunrui) {
	return (Class[hinsi][bunrui].id==NULL)? 
		NullStr: (const char *)Class[hinsi][bunrui].id;
}

///	Get all bunrui
///	@param hinsi Index of hinsi.
///	@param list [out]List of bunrui. It ranges from 1 to return num-1.
///	@return Nunber of list items.
int ext_get_all_bunrui(int hinsi, const char ** list) {
	int i;
	*list++ = NullStr;
	for (i=1 ; Class[hinsi][i].id!=NULL && i<=CLASSIFY_NO; i++) {
		*list++ = Class[hinsi][i].id;
	}
	return i;
}

///	Get katuyou1 string.
///	@param katuyou1 Index of katuyou1.
///	@return String of katuyou1. if index is wrong, return null string.
const char * ext_get_katuyou1(int katuyou1) {
	return (Type[katuyou1].name==NULL)? 
		NullStr: (const char *)Type[katuyou1].name;
}

///	Get all katuyou1
///	@param list [out]List of katuyou1. It ranges from 1 to return num-1.
///	@return Nunber of list items.
int ext_get_all_katuyou1(const char ** list) {
	int i;
	*list++ = NullStr;
	for (i=1 ; Type[i].name!=NULL && i<TYPE_NO; i++) {
		*list++ = Type[i].name;
	}
	return i;
}

///	Get katuyou2 string.
///	@param katuyou1 Index of katuyou1.
///	@param katuyou2 Index of katuyou2.
///	@return String of katuyou2. if index is wrong, return null string.
const char * ext_get_katuyou2(int katuyou1, int katuyou2) {
	return (Form[katuyou1][katuyou2].name==NULL)? 
		NullStr: (const char *)Form[katuyou1][katuyou2].name;
}

///	Get all katuyou2
///	@param katuyou2 Index of katuyou2.
///	@param list [out]List of katuyou2. It ranges from 1 to return num-1.
///	@return Nunber of list items.
int ext_get_all_katuyou2(int katuyou1, const char ** list) {
	int i;
	*list++ = NullStr;
	for (i=1 ; Form[katuyou1][i].name!=NULL && i<FORM_NO; i++) {
		*list++ = Form[katuyou1][i].name;
	}
	return i;
}

///	Get posible max number of params.
///	Those index ranges from 1 to return num-1. 
void ext_get_maxidx(int *pmax_hinsi, int *pmax_bunrui, 
	int *pmax_katuyou1, int *pmax_katuyou2) {
	*pmax_hinsi = CLASSIFY_NO+1;
	*pmax_bunrui = CLASSIFY_NO+1;
	*pmax_katuyou1 = TYPE_NO;
	*pmax_katuyou2 = FORM_NO;
}

