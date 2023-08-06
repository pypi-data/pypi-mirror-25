#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include "encoder.h"

static void enc_stream_init(ENC_STREAM_T *pstream);
static bool enc_stream_set(
	ENC_STREAM_T *pstream, const char * const * pencodings, 
	size_t buff_size, char ** pbuffs);
static bool enc_stream_alloc(ENC_STREAM_T *pstream, int idx);
static void enc_stream_free(ENC_STREAM_T *pstream);
static bool enc_stream_convert(ENC_STREAM_T *pstream);

///	New encoder
///	@param buff_input_write Default buffer to write input. if NULL, newly allocates.
/// @param size_input Size of buffer for input.
///	@param buff_output_read Default buffer to read output. if NULL, newly allocates.
/// @param size_output Size of buffer for output.
/// @return Pointer of encoder. Or NULL, if failed.
ENCODER_T * encoder_new(
	char * buff_input_write, size_t size_input,
	char * buff_output_read, size_t size_output) {
	
	ENCODER_T * penc;
	if(NULL==(penc = malloc(sizeof(ENCODER_T)))) return NULL;
	enc_stream_init(&(penc->in));
	enc_stream_init(&(penc->out));
	//	temporaly store
	penc->in.buff[1] = buff_input_write;
	penc->in.size = size_input;
	penc->out.buff[0] = buff_output_read;
	penc->out.size = size_output;
	return penc;
}

///	Delete encoder
///	@param penc Encoder properties.
void encoder_delete(ENCODER_T *penc) {
	if(NULL==penc) return;
	enc_stream_free(&(penc->in));
	enc_stream_free(&(penc->out));
	free(penc);
}

///	Set encodings
///	@param penc Encoder properties.
/// @param s_inner Name of inner encoding. If NULL or null string, set to UTF-8
/// @param s_inout Comma separated string of input and output encoding.
///	If comma does not exist, both input and output encoding considered this value.
///	If NULL or null string, considered same as inner encoding and will not do encoding.
bool encoder_set_encoding(ENCODER_T *penc, const char * s_inner, const char * s_inout) {
	char s_io[ENC_NAME_LEN*2];
	char * s_incode, * s_outcode;
	const char * encodings[2];
	char * buffers[2];

	if(NULL==s_inner || 0==s_inner[0])	s_inner = "UTF-8";
	s_io[0] = 0;
	if(NULL!=s_inout) strncpy(s_io, s_inout, sizeof(s_io));
	s_io[sizeof(s_io)-1] = 0;
	//	split s_inout
	s_incode = s_outcode = s_io;
	while(*s_outcode!=0 && *s_outcode!=',') s_outcode++;
	if(*s_outcode==',') *s_outcode++ = 0;		
	else s_outcode = s_incode;
	//	set input stream
	encodings[0] = s_incode;
	buffers[0] = NULL;
	encodings[1] = s_inner;
	buffers[1] = penc->in.buff[1];
	if(!enc_stream_set(&(penc->in), encodings,  penc->in.size, buffers)) {
		return false;
	}
	//	set output stream
	encodings[0] = s_inner;
	buffers[0] = penc->out.buff[0];
	encodings[1] = s_outcode;
	buffers[1] = NULL;
	if(!enc_stream_set(&(penc->out), encodings,  penc->out.size, buffers)) {
		return false;
	}
	return true;
}

///	Get input buffer to write.
///	@param penc Encoder properties.
/// @param direction. Stream direction. ENC_IN(0) or ENC_OUT(1)
/// @param port. Port of stream. ENC_WRITE(0) or ENC_READ(1)
///	@param psize [out]Pointer to write buffer size.
/// @return buffer pointer.
char * encoder_getbuff(ENCODER_T *penc, int direction, int port, size_t *psize) {
	ENC_STREAM_T *pstream;
	pstream = direction? &(penc->out): &(penc->in);
	*psize = pstream->size;
	return pstream->buff[port];
}

/// Conver encoding.
///	@param penc Encoder properties.
/// @param direction. ENC_IN(0) or ENC_OUT(1)
/// @return Success or fail
bool encoder_convert(ENCODER_T *penc, int direction) {
	ENC_STREAM_T *pstream;
	const char * s_direc;
	pstream = direction? &(penc->out): &(penc->in);
	s_direc = direction? "output": "input";
	if(false==enc_stream_convert(pstream)) {
		fprintf(stderr, "Fail to convert %s encoding.(%s)\n", s_direc, pstream->buff[0]);
		return false;
	}
	return true;
}

/// Check needs to convert.
///	@param penc Encoder properties.
/// @param direction. ENC_IN or ENC_OUT
/// @return true if needs conversion, or false.
bool encoder_needs(ENCODER_T *penc, int direction) {
	ENC_STREAM_T *pstream;
	pstream = direction? &(penc->out): &(penc->in);
	return (IC_FALSE==pstream->ic)? false: true;
}

/// printf with coverting.
///	@param penc Encoder properties.
///	@param stream stream to output.
/// @param format Format will be filled with following arguments.
/// @return Success or fail
bool encoder_printf(ENCODER_T *penc, FILE * stream, const char * format, ...) {
	va_list va;
	bool result;

	va_start(va, format);
	result = encoder_vprintf(penc, stream, format, va);
	va_end(va);
	return result;
}

/// vprintf with coverting.
///	@param penc Encoder properties.
///	@param stream stream to output.
/// @param format Format.
/// @param va Argumets to fill format with.
/// @return Success or fail
bool encoder_vprintf(ENCODER_T *penc, FILE * stream, const char * format, va_list va) {
	int result;
	ENC_STREAM_T *pstream;

	if(stream==stderr || IC_FALSE==penc->out.ic) {
		vfprintf(stream, format, va);
		return true;
	}
	pstream = &(penc->out);
	result = vsnprintf(pstream->buff[0], pstream->size, format, va);
	if(result<0 || pstream->size<=result) {
		fprintf(stderr, "Fail to fill format in encoder_printf.(%s)\n", format);
		return false;
	}
	if(false==enc_stream_convert(pstream)) {
		fprintf(stderr, "Fail to convert encoding in encoder_printf.(%s)\n", pstream->buff[0]);
		return false;
	}
	fprintf(stream, pstream->buff[1]);
	return true;
}

static void enc_stream_init(ENC_STREAM_T *pstream) {
	pstream->ic = IC_FALSE;
	pstream->size = 0;
	pstream->buff[0] = pstream->buff[1] = NULL;
	pstream->b_alloced[0] = pstream->b_alloced[1] = false;
}

static bool enc_stream_set(
	ENC_STREAM_T *pstream, const char * const * pencodings, 
	size_t buff_size, char ** pbuffs) {

	int i;
	if( pencodings[0][0]==0 || pencodings[1][0]==0
		|| 0==strcasecmp(pencodings[0], pencodings[1])) {

		//	No needs to convert. both buffers are same.
		if(NULL==pbuffs[0] && NULL==pbuffs[1]) {
			if(!enc_stream_alloc(pstream, 0)) return false;
			pstream->buff[1] = pstream->buff[0];
		} else if(NULL==pbuffs[1]) {
			pstream->buff[0] = pstream->buff[1] = pbuffs[0];
		} else {
			pstream->buff[0] = pstream->buff[1] = pbuffs[1];
		}
		return true;
	}
	//	open iconv
	pstream->ic = iconv_open(pencodings[1], pencodings[0]);
	if(IC_FALSE==pstream->ic) {
		fprintf(stderr, "Encoding name(%s or %s) is not avairable.\n", pencodings[0],  pencodings[1]);
		return false;
	}
	//	allocate buffer
	pstream->size = buff_size;
	for(i=0; i<2; i++) {
		pstream->buff[i] = pbuffs[i];
		if(!enc_stream_alloc(pstream, i)) return false;
	}
	return true;
}

static bool enc_stream_alloc(ENC_STREAM_T *pstream, int idx) {
	if(NULL==pstream->buff[idx]) {
		if(NULL==(pstream->buff[idx] = malloc(pstream->size))) {
			fprintf(stderr, "Fail to allocate buffer in encoder.\n");
			return false;
		}
		pstream->b_alloced[idx] = true;
	}
	return true;
}

static void enc_stream_free(ENC_STREAM_T *pstream) {
	int i;
	if(IC_FALSE != pstream->ic)	{
		iconv_close(pstream->ic);
		pstream->ic = IC_FALSE;
	}
	for(i=0; i<2; i++) {
		if(pstream->b_alloced[i]) {
			free(pstream->buff[i]);
			pstream->b_alloced[i] = false;
		}
	}	
}

static bool enc_stream_convert(ENC_STREAM_T *pstream) {
	char *pinbuf, *poutbuf;
	size_t inbuf_size, outbuf_size, result;

	if(IC_FALSE==pstream->ic) return true;	//	nothing to do
	pinbuf = pstream->buff[0];
	poutbuf = pstream->buff[1];
	inbuf_size = strlen(pinbuf);
	outbuf_size = pstream->size - 1;
	result = iconv(pstream->ic, &pinbuf, &inbuf_size, &poutbuf, &outbuf_size );
	*poutbuf = 0;
	return ((size_t)-1 == result)? false: true;
}
