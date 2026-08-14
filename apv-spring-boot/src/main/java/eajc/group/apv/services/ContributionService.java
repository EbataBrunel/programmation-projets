package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.Event;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

public interface ContributionService {
    // CREATE
    ContributionResponseDto createContribution(ContributionRequestDto dto, Long userId);

    // READ
    List<ContributionResponseDto> getAllContributions();

    // GET
    ContributionResponseDto getContributionByPublicId(UUID publicId);

    // UPDATE
    ContributionResponseDto updateContribution(UUID publicId, ContributionRequestDto dto, Long userId);

    // GET
    List<EventTypeContributionCountDto> countEventByEventTypeWithContribution();

    // GET
    public List<ContributionsByEventCountDto> countContributionsByEventAndEventType(UUID eventTypePublicId);

    // GET
    public BigDecimal calculateEventTotal(Long eventId);

    // GET
    void updateEventAmountTotal(Event event);

    // GET
    List<ContributionResponseDto> getContributionsByEvent(UUID eventPublicId);

    // GET
    List<ContributionResponseDto> getContributionsByContributed(UUID contributedPublicId);

    // GET
    public List<ContributedCountDTO> countContributionsByContributed();

    // GET
    List<ContributionCountByEventTypeDTO> countContributionsByEventType();

    // GET
    public byte[] exportPdf() throws Exception;
    // DELETE
    void deleteContribution(UUID publicId);
}
