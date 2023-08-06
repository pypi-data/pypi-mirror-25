#ifndef EXT_API_H
#define EXT_API_H

#ifdef __cplusplus
extern "C" {
#endif

#define DEF_MAX_ITEMS	(1000)

typedef struct ext_mrph_t {
	const char * midasi1;
	const char * yomi;
	const char * midasi2;
	int hinsi;
	int bunrui;
	int katuyou1;
	int katuyou2;
} EXT_MRPH_T;

typedef enum ext_res_code {
	EXT_SUCCESS = 0,
	EXT_MRPH_BUFF_OVER,
	EXT_WORD_BUFF_OVER,
	EXT_ERROR = 100,
	EXT_RC_ERROR,
	EXT_MALLOC_ERROR,
	EXT_FILE_NOT_EXISTS,
	EXT_ANA_ERROR,
} EXT_RES_CODE;

///	Set encoding
///	It must be called before ext_init.
///	If specified wrong encoding name, error will occure in ext_init.
/// @param s_encoding Comma separated string of input and output encoding.
///	If comma does not exist, both input and output encoding considered this value.
///	If NULL or null string, considered same as inner encoding and will not do encoding.
extern void ext_set_encoding(const char *s_encoding);

///	Initialize lib
///	@param s_rcfile	Path to jumanrc
///	@param word_buf_size Word buffer size. It is copied midasi1, yomi, and midasi2.
///	@param max_mrphs Morpheme buffer size in number. 
///	@return 
///	- EXT_SUCCESS:	Success 
///	- EXT_RC_ERROR:	Resource file error.
///	- EXT_MALLOC_ERROR:	Cannot allocate memory.
extern EXT_RES_CODE ext_init(const char *s_rcfile, size_t word_buf_size, int max_mrphs);

///	Close extlib
extern void ext_close();
	
///	Get input buffer to write.
///	@param psize [out]Buffer size.
///	@return Buffer address.
extern char * ext_get_input_buff(size_t *psize);

///	Get morpheme buffer to read.
///	@return Buffer address.
extern EXT_MRPH_T * ext_get_mrph_buff();

///	Analyze with best path
///	@return 
///	- EXT_SUCCESS:	Success 
///	- EXT_ERROR:	Error
extern EXT_RES_CODE ext_analyze();

///	Get result in mopheme buffer
///	@param pnum_mrphs [out]Number of mopheme in buffer
///	@return 
///	- EXT_SUCCESS:	Put all morpheme.
///	- EXT_WORD_BUFF_OVER:	Word buffer is not enough. Call more to get all morpheme.
///	- EXT_MRPH_BUFF_OVER:	Morpheme buffer is not enough. Call more to get all morpheme.
extern EXT_RES_CODE ext_get_result(int *pnum_mrphs);

///	Get hinsi string.
///	@param hinsi Index of hinsi.
///	@return String of bunrui. if index is wrong, return null string.
extern const char * ext_get_hinsi(int hinsi);

///	Get all hinsi
///	@param list [out]List of hinsi. It ranges from 1 to return num-1.
///	@return Nunber of list items.
extern int ext_get_all_hinsi(const char ** list);

///	Get bunrui string.
///	@param hinsi Index of hinsi.
///	@param bunrui Index of bunrui.
///	@return String of bunrui. if index is wrong, return null string.
extern const char * ext_get_bunrui(int hinsi, int bunrui);

///	Get all bunrui
///	@param hinsi Index of hinsi.
///	@param list [out]List of bunrui. It ranges from 1 to return num-1.
///	@return Nunber of list items.
extern int ext_get_all_bunrui(int hinsi, const char ** list);

///	Get katuyou1 string.
///	@param katuyou1 Index of katuyou1.
///	@return String of katuyou1. if index is wrong, return null string.
extern const char * ext_get_katuyou1(int katuyou1);

///	Get all katuyou1
///	@param list [out]List of katuyou1. It ranges from 1 to return num-1.
///	@return Nunber of list items.
extern int ext_get_all_katuyou1(const char ** list);

///	Get katuyou2 string.
///	@param katuyou1 Index of katuyou1.
///	@param katuyou2 Index of katuyou2.
///	@return String of katuyou2. if index is wrong, return null string.
extern const char * ext_get_katuyou2(int katuyou1, int katuyou2);

///	Get all katuyou2
///	@param katuyou2 Index of katuyou2.
///	@param list [out]List of katuyou2. It ranges from 1 to return num-1.
///	@return Nunber of list items.
extern int ext_get_all_katuyou2(int katuyou1, const char ** list);

///	Get posible max number of params.
///	Those index ranges from 1 to return num-1. 
extern void ext_get_maxidx(int *pmax_hinsi, int *pmax_bunrui, 
	int *pmax_katuyou1, int *pmax_katuyou2);

#ifdef __cplusplus
}
#endif

#endif	//	EXT_API_H

