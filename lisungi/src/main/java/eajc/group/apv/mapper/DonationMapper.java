package eajc.group.apv.mapper;

import eajc.group.apv.dto.DonationParticipantResponseDto;
import eajc.group.apv.dto.DonationRequestDto;
import eajc.group.apv.dto.DonationResponseDto;
import eajc.group.apv.entity.Beneficiary;
import eajc.group.apv.entity.DonationParticipant;
import eajc.group.apv.entity.Donation;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DonationMapper {

    public Donation toEntity(DonationRequestDto dto, Beneficiary beneficiary, String filename){
        Donation donation = new Donation();

        donation.setTitle(dto.getTitle());
        donation.setDescription(dto.getDescription());
        donation.setDateDonation(dto.getDateDonation());
        donation.setBeneficiary(beneficiary);
        donation.setPhoto(filename);

        return  donation;
    }

    private DonationParticipantResponseDto toDonationParticipantDto(DonationParticipant participant) {
        DonationParticipantResponseDto dto = new DonationParticipantResponseDto();
        dto.setPublicId(participant.getPublicId());
        dto.setName(participant.getName());
        dto.setDescription(participant.getDescription());
        dto.setDonationTitle(participant.getDonation().getTitle());
        dto.setParticipationDate(participant.getParticipationDate());
        return dto;
    }

    public DonationResponseDto toDto(Donation donation){

        DonationResponseDto dto = new DonationResponseDto();
        dto.setId(donation.getId());
        dto.setPublicId(donation.getPublicId());
        dto.setTitle(donation.getTitle());
        dto.setDescription(donation.getDescription());
        dto.setDateDonation(donation.getDateDonation());
        dto.setPhoto(donation.getPhoto());
        dto.setClosure_status(donation.getClosure_status());
        dto.setPublicStatus(donation.getPublicStatus());
        dto.setBeneficiaryId(donation.getBeneficiary().getId());
        dto.setBeneficiaryName(donation.getBeneficiary().getName());
        dto.setParticipants(donation.getParticipants() == null
                ? List.of()
                : donation.getParticipants()
                .stream()
                .map(this::toDonationParticipantDto)
                .toList()
        );

        return  dto;
    }
}
