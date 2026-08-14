package eajc.group.apv.services;

import eajc.group.apv.dto.EventCountByYearDto;
import eajc.group.apv.dto.EventRequestDto;
import eajc.group.apv.dto.EventResponseDto;
import eajc.group.apv.dto.EventTypeCountDto;
import eajc.group.apv.entity.Event;
import eajc.group.apv.entity.EventType;
import eajc.group.apv.entity.User;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.EventMapper;
import eajc.group.apv.repository.EventRepository;
import eajc.group.apv.repository.EventTypeRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.Year;
import java.time.YearMonth;
import java.util.List;
import java.util.UUID;

@Service
public class EventServiceImpl implements EventService{

    private final EventRepository eventRepository;
    private final EventMapper eventMapper;
    private final UserRepository userRepository;
    private final EventTypeRepository eventTypeRepository;


    public EventServiceImpl(EventRepository eventRepository, EventMapper eventMapper, UserRepository userRepository, EventTypeRepository eventTypeRepository) {
        this.eventRepository = eventRepository;
        this.eventMapper = eventMapper;
        this.userRepository = userRepository;
        this.eventTypeRepository = eventTypeRepository;
    }

    @Override
    public EventResponseDto createEvent(EventRequestDto dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if (dto.getEventDate() == null) {
            throw new BadRequestException("La date est obligatoire.");
        }

        User user = userRepository.findById(dto.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        EventType eventType = eventTypeRepository.findById(dto.getEventTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Type d'évènement introuvable"));

        // Vérification doublon user + eventType
        if (eventRepository.existsByUserIdAndEventTypeId(
                user.getId(),
                eventType.getId()
        )) {
            throw new BadRequestException(
                    "Cet utilisateur possède déjà un événement de ce type."
            );
        }

        Event event = eventMapper.toEntity(dto, eventType, user);
        Event eventSave = eventRepository.save(event);
        return eventMapper.toDto(eventSave);
    }

    @Override
    public List<EventResponseDto> getAllEvents() {
        return eventRepository.findAll()
                .stream()
                .map(eventMapper::toDto)
                .toList();
    }

    @Override
    public EventResponseDto getEventByPublicId(UUID publicId) {
        Event event = eventRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));
        return eventMapper.toDto(event);
    }

    @Override
    public EventResponseDto getEventById(Long id) {
        Event event = eventRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));
        return eventMapper.toDto(event);
    }

    @Override
    public List<EventTypeCountDto> countEventsByEventType() {
        return eventRepository.countEventsByEventType()
                .stream()
                .map(obj -> new EventTypeCountDto(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (Long) obj[3]
                ))
                .toList();
    }

    @Override
    public List<EventResponseDto> findByEventTypeId(Long eventTypeId) {
        return eventRepository.findByEventTypeId(eventTypeId)
                .stream()
                .map(eventMapper::toDto)
                .toList();
    }

    @Override
    public List<EventCountByYearDto> countEventsByYear() {
        return eventRepository.countEventsByYear()
                .stream()
                .map(obj -> new EventCountByYearDto(
                        (Integer) obj[0],
                        (Long) obj[1]
                ))
                .toList();
    }

    @Override
    public List<EventResponseDto> getEventsByMonth(int year, int month) {
        YearMonth yearMonth = YearMonth.of(year, month);

        LocalDate startDate = yearMonth.atDay(1);
        LocalDate endDate = yearMonth.atEndOfMonth();

        return eventRepository.findByEventDateBetween(startDate, endDate)
                .stream()
                .map(eventMapper::toDto)
                .toList();
    }

    @Override
    public List<EventResponseDto> getEventsByYear(int year) {
        Year targetYear = Year.of(year);

        LocalDate startDate = targetYear.atDay(1);
        LocalDate endDate = targetYear.atDay(targetYear.length());

        return eventRepository.findByEventDateBetween(startDate, endDate)
                .stream()
                .map(eventMapper::toDto)
                .toList();
    }

    @Override
    public EventResponseDto updateClosureStatusEvent(UUID publicId){
        Event event = eventRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));

        event.setClosure_status(true);
        return eventMapper.toDto(eventRepository.save(event));

    }

    @Override
    public EventResponseDto updateEvent(UUID publicId, EventRequestDto dto) {

        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom de l'événement est obligatoire.");
        }

        if (dto.getEventDate() == null) {
            throw new BadRequestException("La date est obligatoire.");
        }

        User user = userRepository.findById(dto.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        EventType eventType = eventTypeRepository.findById(dto.getEventTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        // Vérification doublon user + eventType
        if (eventRepository.existsByUserIdAndEventTypeIdAndPublicIdNot(
                user.getId(),
                eventType.getId(),
                publicId
        )) {
            throw new BadRequestException(
                    "Cet utilisateur possède déjà un événement de ce type."
            );
        }

        Event event = eventRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Evènement  introuvable"));

        event.setName(dto.getName());
        event.setMount(dto.getMount());
        event.setEventDate(dto.getEventDate());
        event.setComment(dto.getComment());
        event.setEventType(eventType);
        event.setUser(user);

        return eventMapper.toDto(eventRepository.save(event));
    }

    @Override
    public void deleteEvent(UUID publicId) {
        Event event = eventRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));

        eventRepository.delete(event);
    }
}
