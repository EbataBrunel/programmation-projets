package eajc.group.apv.services;

import eajc.group.apv.dto.EventCountByYearDto;
import eajc.group.apv.dto.EventRequestDto;
import eajc.group.apv.dto.EventResponseDto;
import eajc.group.apv.dto.EventTypeCountDto;
import eajc.group.apv.entity.Event;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public interface EventService {
    // CREATE
    EventResponseDto createEvent(EventRequestDto dto);

    // READ
    List<EventResponseDto> getAllEvents();

    // GET
    EventResponseDto getEventByPublicId(UUID publicId);

    // GET
    EventResponseDto getEventById(Long id);

    // GET
    public List<EventTypeCountDto> countEventsByEventType();

    // GET
    List<EventResponseDto> findByEventTypeId(Long eventTypeId);

    // GET
    List<EventCountByYearDto> countEventsByYear();

    // GET
    List<EventResponseDto> getEventsByMonth(int year, int month);

    // GET
    List<EventResponseDto> getEventsByYear(int year);

    // UPDATE
    EventResponseDto updateClosureStatusEvent(UUID publicId);

    // UPDATE
    EventResponseDto updateEvent(UUID publicId, EventRequestDto dto);

    // DELETE
    void deleteEvent(UUID publicId);
}
