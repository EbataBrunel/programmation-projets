package eajc.group.apv.mapper;

import eajc.group.apv.dto.DonationParticipantRequestDto;
import eajc.group.apv.dto.DonationParticipantResponseDto;
import eajc.group.apv.entity.Donation;
import eajc.group.apv.entity.DonationParticipant;
import eajc.group.apv.entity.User;
import org.springframework.stereotype.Component;

@Component
public class DonationParticipantMapper {

    public DonationParticipant toEntity(DonationParticipantRequestDto dto, Donation donation, User user){

        DonationParticipant participant = new DonationParticipant();

        participant.setName(dto.getName().trim());
        participant.setDescription(dto.getDescription().trim());
        participant.setAmount(participant.getAmount());
        participant.setDonation(donation);
        participant.setUser(user);
        participant.setItemType(dto.getItemType());

        return  participant;
    }

    public DonationParticipantResponseDto toDto(DonationParticipant donationParticipant){

        DonationParticipantResponseDto dto = new DonationParticipantResponseDto();

        dto.setId(donationParticipant.getId());
        dto.setPublicId(donationParticipant.getPublicId());
        dto.setName(donationParticipant.getName());
        dto.setDescription(donationParticipant.getDescription());
        dto.setAmount(donationParticipant.getAmount());
        dto.setParticipationDate(donationParticipant.getParticipationDate());
        dto.setDonationId(donationParticipant.getDonation().getId());
        dto.setUserId(dto.getUserId());
        dto.setUserLastName(donationParticipant.getUser().getProfile().getLastName());
        dto.setUserFirstName(donationParticipant.getUser().getProfile().getFirstName());
        dto.setItemType(donationParticipant.getItemType().name());

        return  dto;
    }
}
