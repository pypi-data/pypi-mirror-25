#pragma once

#include <stdint.h>
#include <vector>

void init_logging(MblMwMetaWearBoard *board);
void tear_down_logging(void *state, bool preserve_memory);
void serialize_logging(const MblMwMetaWearBoard* board, std::vector<uint8_t>& state);
void deserialize_logging(MblMwMetaWearBoard* board, bool deserialize_component, uint8_t** state_stream);
void disconnect_logging(MblMwMetaWearBoard* board);
int64_t calculate_epoch(const MblMwMetaWearBoard* board, uint32_t tick);
