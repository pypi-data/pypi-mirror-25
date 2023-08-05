#include <glib.h>
#include <gst/gst.h>


static gboolean g_object_get_bool(GstElement *element, char *name)
{
    gboolean value;
    g_object_get(G_OBJECT(element), name, &value, NULL);
    return value;
}

static GstSample *c_appsink_pull_preroll(GstElement *appsink)
{
	GstSample *sample = NULL;
	g_signal_emit_by_name(appsink, "pull-preroll", &sample);
    return sample;
}

static GstSample *c_appsink_pull_sample(GstElement *appsink)
{
	GstSample *sample = NULL;
	g_signal_emit_by_name(appsink, "pull-sample", &sample);
    return sample;
}

typedef void (*appcallback_t)(void *, int, int, char *, int);
typedef void (*buscallback_t)(void *, GstMessage *);
typedef struct {
	appcallback_t callback;
	buscallback_t bcallback;
	char eventname[15];
	PyObject *userdata;
} callback_data_t;

static void c_signal_disconnect(GstElement *element, gulong handler_id)
{
	g_signal_handler_disconnect(element, handler_id);
}

