#pragma once

// Flags
enum {
	STRAT_FLAG_STOP = (1 << 0),
};

// Main strat thing
typedef struct Strat {
	char *ip;
	char *memory;
	int flags;
} Strat;

// Strat jump table function type
typedef void (*StratFunc)(Strat *this);

// Functions
void StratInit(Strat *this, char *memory);
void StratIncIP(Strat *this);
void StratSetFlag(Strat *this, int flags);
int16_t StratReadShort(Strat *this);
int32_t StratReadLong(Strat *this);
void StratRun(Strat *this);
