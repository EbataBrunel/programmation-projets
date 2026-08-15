package eajc.group.apv.services;

import eajc.group.apv.dto.EventTypeRequestDto;
import eajc.group.apv.dto.EventTypeResponseDto;

import java.util.List;
import java.util.UUID;

public interface EventTypeService {
    // CREATE
    EventTypeResponseDto createEventType(EventTypeRequestDto dto);

    // READ
    List<EventTypeResponseDto> getAllEventTypes();

    // GET
    EventTypeResponseDto getEventTypeByPublicId(UUID publicId);

    // UPDATE
    EventTypeResponseDto updateEventType(UUID publicId, EventTypeRequestDto dto);

    // DELETE
    void deleteEventType(UUID publicId);
}
