#include "util/log.h"
#include "util/storage.h"
#include "util/storage_filesystem.h"
#include "util/file.h"
#include "util/alloc.h"
#include "util/args.h"

#include "strat.h"

static DgError OsInitMelon(void) {
	// Set up storage pool(s)
	DgError status = DgStorageAddPool(NULL, DgFilesystemCreatePool("file", "./"));
	
	if (status) {
		return status;
	}
	
	return DG_ERROR_SUCCESS;
}

int main(int argc, char *argv[]) {
	DgError status;
	
	// Startup message
	DgLog(DG_LOG_INFO, "OpenStrat v0.0.1");
	
	// Parse command line arguments
	DgArgs args;
	DgArgParse(&args, argc, argv);
	
	// Initialise the melon library
	if (OsInitMelon()) {
		DgLog(DG_LOG_ERROR, "Failed to initailse melon library.");
		return 1;
	}
	
	// Get file name
	const char *path = DgArgGetValue(&args, "i");
	
	if (!path) {
		DgLog(DG_LOG_ERROR, "You did not specify a file path. To add one, use '-i <file path>'.");
		return 1;
	}
	
	// Load the strat file
	size_t length;
	char *data;
	
	DgLog(DG_LOG_INFO, "Loading file: %s", path);
	
	status = DgFileLoad(NULL, path, &length, &data);
	
	if (status) {
		DgLog(DG_LOG_ERROR, "Failed to load the file at %s.", path);
		return 1;
	}
	
	// Run the strat
	Strat strat;
	
	StratInit(&strat, data);
	StratRun(&strat);
	
	// Free data
	DgFree(data);
	
	DgLog(DG_LOG_SUCCESS, "Done!");
	
	return 0;
}
