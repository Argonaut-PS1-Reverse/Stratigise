#include <inttypes.h>
#include "util/log.h"

#include "strat.h"

static void stCommandError(Strat *this) {
	StratIncIP(this);
	DgLog(DG_LOG_ERROR, "stCommandError");
	StratSetFlag(this, STRAT_FLAG_STOP);
}

StratFunc strat_jump_table[] = {
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
	stCommandError,
};

void StratInit(Strat *this, char *memory) {
	/**
	 * Initialise a strategy
	 */
	
	this->memory = memory;
	this->ip = this->memory + 8;
}

void StratIncIP(Strat *this) {
	/**
	 * Increment the instruction pointer
	 */
	
	this->ip += 1;
}

void StratSetFlag(Strat *this, int flags) {
	/**
	 * Set a flag on the strat
	 */
	
	this->flags |= flags;
}

int16_t StratReadShort(Strat *this) {
	/**
	 * Read a 16-bit integer form memory
	 */
	
	return *(this->ip++) + (*(this->ip++) << 8);
}

int32_t StratReadLong(Strat *this) {
	/**
	 * Read a 32-bit ineger from memory
	 */
	
	return *(this->ip++) + (*(this->ip++) << 8) + (*(this->ip++) << 16) + (*(this->ip++) << 24);
}

void StratRun(Strat *this) {
	/**
	 * Run a strat bytecode
	 */
	
	while ((this->flags & STRAT_FLAG_STOP) == 0) {
		int opcode = (int) *this->ip;
		DgLog(DG_LOG_VERBOSE, "opcode %d (0x%x)", opcode, opcode);
		(strat_jump_table[opcode])(this);
	}
	
	DgLog(DG_LOG_INFO, "Strat execution stopped.");
}
