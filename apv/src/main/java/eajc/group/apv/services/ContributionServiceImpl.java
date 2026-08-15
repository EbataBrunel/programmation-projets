package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.Contribution;
import eajc.group.apv.entity.Event;
import eajc.group.apv.entity.User;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.ContributionMapper;
import eajc.group.apv.repository.ContributionRepository;
import eajc.group.apv.repository.EventRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Service
public class ContributionServiceImpl implements ContributionService{
    private final ContributionRepository contributionRepository;
    private final ContributionMapper contributionMapper;
    private final UserRepository userRepository;
    private final EventRepository eventRepository;
    private final ContributionPdfService pdfService;

    public ContributionServiceImpl(ContributionRepository contributionRepository, ContributionMapper contributionMapper, UserRepository userRepository, EventRepository eventRepository, ContributionPdfService pdfService) {
        this.contributionRepository = contributionRepository;
        this.contributionMapper = contributionMapper;
        this.userRepository = userRepository;
        this.eventRepository = eventRepository;
        this.pdfService = pdfService;
    }


    @Override
    @Transactional
    public ContributionResponseDto createContribution(ContributionRequestDto dto, Long userId) {
        if (dto.getAmount() == null) {
            throw new BadRequestException("Le montant est obligatoire.");
        }

        // Vérification doublon contributor + event
        if (contributionRepository.existsByContributedIdAndEventId(
                dto.getContributedId(),
                dto.getEventId()
        )) {
            throw new BadRequestException(
                    "Cet utilisateur a déjà contribué pour cet événement."
            );
        }

        User contributed = userRepository.findById(dto.getContributedId())
                .orElseThrow(() -> new ResourceNotFoundException("Contributeur introuvable"));

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        Event event = eventRepository.findById(dto.getEventId())
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));

        if (event.getClosure_status()){
            throw new BadRequestException("Cet évènement a déjà été clôturé.");
        }

        Contribution contribution = contributionMapper.toEntity(dto, contributed, event, user);
        Contribution contributionSave = contributionRepository.save(contribution);

        // Mettre ç jour le montant total de l'évènement
        Event eventSave = contribution.getEvent();

        updateEventAmountTotal(eventSave);

        return contributionMapper.toDto(contributionSave);
    }

    @Override
    public List<ContributionResponseDto> getAllContributions() {
        return contributionRepository.findAll()
                .stream()
                .map(contributionMapper::toDto)
                .toList();
    }

    @Override
    public ContributionResponseDto getContributionByPublicId(UUID publicId) {
        Contribution event = contributionRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contribution introuvable"));
        return contributionMapper.toDto(event);
    }

    @Override
    public List<ContributionsByEventCountDto> countContributionsByEventAndEventType(UUID eventTypePublicId) {
        return contributionRepository.countContributionsByEventAndEventType(eventTypePublicId)
                .stream()
                .map(obj -> new ContributionsByEventCountDto(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (Boolean) obj[3],
                        (BigDecimal) obj[4],
                        (BigDecimal) obj[5],
                        (Long) obj[6]
                ))
                .toList();
    }

    @Override
    public BigDecimal calculateEventTotal(Long eventId) {
        return contributionRepository.sumContributionsByEvent(eventId);
    }

    @Override
    public void updateEventAmountTotal(Event event) {
        BigDecimal total = contributionRepository
                .sumContributionsByEvent(event.getId());

        event.setAmountTotal(total);

        eventRepository.save(event);
    }


    @Override
    @Transactional
    public ContributionResponseDto updateContribution(UUID publicId, ContributionRequestDto dto, Long userId) {
        if (dto.getAmount() == null) {
            throw new BadRequestException("Le montant est obligatoire.");
        }

        // Vérification doublon contributor + event
        if (contributionRepository.existsByContributedIdAndEventIdAndPublicIdNot(
                dto.getContributedId(),
                dto.getEventId(),
                publicId
        )) {
            throw new BadRequestException(
                    "Cet utilisateur a déjà contribué pour cet événement."
            );
        }

        User contributed = userRepository.findById(dto.getContributedId())
                .orElseThrow(() -> new ResourceNotFoundException("Contributeur introuvable"));

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("Utilisateur introuvable"));

        Event event = eventRepository.findById(dto.getEventId())
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));

        // Récupérer la contribution existante
        Contribution contribution = contributionRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contribution introuvable"));

        // Ancien événement
        Event oldEvent = contribution.getEvent();

        if (event.getClosure_status()){
            throw new BadRequestException("Cet évènement a déjà été clôturé.");
        }

        contribution.setAmount(dto.getAmount());
        contribution.setEvent(event);
        contribution.setContributed(contributed);
        contribution.setUser(user);

        if (event.getMount()
                .compareTo(dto.getAmount()) <= 0) {
            contribution.setStatus(true);
        } else {
            contribution.setStatus(false);
        }

        Contribution savedContribution = contributionRepository.save(contribution);

        // Recalcul du nouvel événement
        updateEventAmountTotal(event);

        // Si l'événement a changé, recalcul de l'ancien
        if (!oldEvent.getId().equals(event.getId())) {
            updateEventAmountTotal(oldEvent);
        }

        return contributionMapper.toDto(savedContribution);
    }

    @Override
    public List<EventTypeContributionCountDto> countEventByEventTypeWithContribution() {
        return contributionRepository.countEventByEventTypeWithContribution()
                .stream()
                .map(obj -> new EventTypeContributionCountDto(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (Long) obj[3]
                ))
                .toList();
    }

    @Override
    public List<ContributionResponseDto> getContributionsByEvent(UUID eventPublicId) {
        Event event = eventRepository.findByPublicId(eventPublicId)
                .orElseThrow(() -> new ResourceNotFoundException("Evènement introuvable"));

        return contributionRepository.findByEventId(event.getId())
                .stream()
                .map(contributionMapper::toDto)
                .toList();
    }

    @Override
    public List<ContributionResponseDto> getContributionsByContributed(UUID contributedPublicId) {
        User user = userRepository.findByPublicId(contributedPublicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contributeur introuvable"));

        return contributionRepository.findByContributedId(user.getId())
                .stream()
                .map(contributionMapper::toDto)
                .toList();
    }

    @Override
    public List<ContributedCountDTO> countContributionsByContributed() {
        return contributionRepository.countContributionsByContributed()
                .stream()
                .map(obj -> new ContributedCountDTO(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (String) obj[3],
                        (Long) obj[4]
                ))
                .toList();
    }

    @Override
    public List<ContributionCountByEventTypeDTO> countContributionsByEventType() {
        return contributionRepository.countContributionsByEventType()
                .stream()
                .map(obj -> new ContributionCountByEventTypeDTO(
                        (Long) obj[0],
                        (UUID) obj[1],
                        (String) obj[2],
                        (Long) obj[3]
                ))
                .toList();
    }

    @Override
    public byte[] exportPdf() throws Exception {
        List<ContributionPdfDto> list =
                contributionRepository.findAll()
                        .stream()
                        .map(contributionMapper::toDtoPDF)
                        .toList();

        return pdfService.generate(list);
    }

    @Override
    public void deleteContribution(UUID publicId) {
        Contribution contribution = contributionRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Contribution introuvable"));

        contributionRepository.delete(contribution);
    }
}
