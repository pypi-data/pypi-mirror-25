#ifndef ENCODER_H
#define ENCODER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stdbool.h>
#include <iconv.h>


//	Length of encoding name;
#define ENC_NAME_LEN	(22)
//	Direction of stream
#define ENC_IN (0)
#define ENC_OUT (1)
//	Port of stream
#define ENC_WRITE (0)
#define ENC_READ (1)

typedef struct enc_stream_t {
	iconv_t ic;			///	iconv descripter
	char *	buff[2];	///	buffers.
	bool b_alloced[2];	///	buff is allocated
	size_t	size;		///	buffer size
} ENC_STREAM_T;

///	Properties
typedef struct encoder_t {
	ENC_STREAM_T	in;
	ENC_STREAM_T	out;
} ENCODER_T;

#define IC_FALSE	((iconv_t)-1)
///	ENCODER_NEEDS is same as encoder_needs
///	but fast and will be optimized
#define ENCODER_NEEDS(penc, direction) ( \
	(((direction)? (penc)->out: (penc)->in).ic==IC_FALSE)? false: true \
)

///	New encoder
///	@param buff_input_write Default buffer to write input. if NULL, newly allocates.
/// @param size_input Size of buffer for input.
///	@param buff_output_read Default buffer to read output. if NULL, newly allocates.
/// @param size_output Size of buffer for output.
/// @return Pointer of encoder. Or NULL, if failed.
ENCODER_T * encoder_new(
	char * buff_input_write, size_t size_input,
	char * buff_output_read, size_t size_output);

///	Delete encoder
///	@param penc Encoder properties.
void encoder_delete(ENCODER_T *penc);

///	Set encodings
///	@param penc Encoder properties.
/// @param s_inner Name of inner encoding. If NULL or null string, set to UTF-8
/// @param s_inout Comma separated string of input and output encoding.
///	If comma does not exist, both input and output encoding considered this value.
///	If NULL or null string, considered same as inner encoding and will not do encoding.
bool encoder_set_encoding(ENCODER_T *penc, 
	const char * s_inner, const char * s_inout);

///	Get input buffer to write.
///	@param penc Encoder properties.
/// @param direction. Stream direction. ENC_IN(0) or ENC_OUT(1)
/// @param port. Port of stream. ENC_WRITE(0) or ENC_READ(1)
///	@param psize [out]Pointer to write buffer size.
/// @return buffer pointer.
extern char * encoder_getbuff(ENCODER_T *penc, 
	int direction, int port, size_t *psize);

/// Conver encoding.
///	@param penc Encoder properties.
/// @param direction. ENC_IN(0) or ENC_OUT(1)
/// @return Success or fail
extern bool encoder_convert(ENCODER_T *penc, int direction);

/// Check needs to convert.
///	@param penc Encoder properties.
/// @param direction. ENC_IN or ENC_OUT
/// @return true if needs conversion, or false.
extern bool encoder_needs(ENCODER_T *penc, int direction);

/// printf with coverting.
///	@param penc Encoder properties.
///	@param stream stream to output.
/// @param format Format will be filled with following arguments.
/// @return Success or fail
bool encoder_printf(ENCODER_T *penc, 
	FILE * stream, const char * format, ...);

/// vprintf with coverting.
///	@param penc Encoder properties.
///	@param stream stream to output.
/// @param format Format.
/// @param va Argumets to fill format with.
/// @return Success or fail
extern bool encoder_vprintf(ENCODER_T *penc, 
	FILE * stream, const char * format, va_list va);

#ifdef __cplusplus
}
#endif

#endif	//	ENCODER_H
