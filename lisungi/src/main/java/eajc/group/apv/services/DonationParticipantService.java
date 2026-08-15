package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public interface DonationParticipantService {
    // CREATE
    DonationParticipantResponseDto createDonationParticipant(DonationParticipantRequestDto dto, Long userId);

    // READ
    List<DonationParticipantResponseDto> getAllDonationParticipants();

    // GET
    DonationParticipantResponseDto getDonationParticipantByPublicId(UUID publicId);

    // UPDATE
    DonationParticipantResponseDto updateDonationParticipant(UUID publicId, DonationParticipantRequestDto dto, Long userId);

    // GET
    List<BeneficiaryDonationParticipantCountDto> countDonationByBeneficiaryWithParticipant();

    // GET
    public List<ParticipantsByDonationCountDto> countParticipantsByDonationAndBeneficiary(UUID beneficiaryPublicId);

    // GET
    List<DonationParticipantResponseDto> getParticipantsByDonation(UUID donationPublicId);

    // DELETE
    void deleteDonationParticipant(UUID publicId);
}
