package eajc.group.apv.mapper;


import eajc.group.apv.dto.ContributionPdfDto;
import eajc.group.apv.dto.ContributionRequestDto;
import eajc.group.apv.dto.ContributionResponseDto;
import eajc.group.apv.entity.Contribution;
import eajc.group.apv.entity.Event;
import eajc.group.apv.entity.User;
import org.springframework.stereotype.Component;

@Component
public class ContributionMapper {

    public Contribution toEntity(ContributionRequestDto dto, User contributed, Event event, User user){
        Contribution contribution = new Contribution();
        contribution.setContributed(contributed);
        contribution.setEvent(event);
        contribution.setAmount(dto.getAmount());
        contribution.setUser(user);
        contribution.setStatus(dto.getStatus());
        return contribution;
    }

    public ContributionResponseDto toDto(Contribution contribution){
        ContributionResponseDto dto = new ContributionResponseDto();
        dto.setPublicId(contribution.getPublicId());
        dto.setContributedId(contribution.getContributed().getId());
        dto.setEventId(contribution.getEvent().getId());
        dto.setEventName(contribution.getEvent().getName());
        dto.setAmount(contribution.getAmount());
        dto.setCreatedAt(contribution.getCreatedAt());
        dto.setStatus(contribution.getStatus());
        dto.setUserId(contribution.getUser().getId());
        dto.setUserLastName(contribution.getUser().getProfile().getLastName());
        dto.setUserFirstName(contribution.getUser().getProfile().getFirstName());

        return  dto;
    }

    public ContributionPdfDto toDtoPDF(Contribution contribution){

        ContributionPdfDto dto = new ContributionPdfDto();

        dto.setPublicId(contribution.getPublicId());

        dto.setContributedName(
                contribution.getContributed().getProfile().getLastName()+" "+contribution.getUser().getProfile().getFirstName());

        dto.setBeneficiaryName(
                contribution.getEvent().getUser().getProfile().getLastName()+" "+contribution.getEvent().getUser().getProfile().getFirstName());

        dto.setEventName(
                contribution.getEvent().getName());

        dto.setMontant(contribution.getAmount());

        dto.setStatut(contribution.getStatus() ? "Payée":"En attente");

        dto.setDate(contribution.getCreatedAt());

        return dto;
    }
}
