package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

public interface DonationService {
    // CREATE
    DonationResponseDto createDonation(DonationRequestDto dto, MultipartFile photoFile) throws IOException;

    // READ
    List<DonationResponseDto> getAllDonations();

    // GET
    DonationResponseDto getDonationByPublicId(UUID publicId);

    // GET
    DonationResponseDto getDonationById(Long id);

    // GET
    public List<BeneficiaryCountDto> countDonationsByBeneficiary();

    // GET
    List<DonationResponseDto> findByBeneficiaryId(Long beneficiaryId);

    // GET
    List<DonationCountByYearDto> countDonationsByYear();

    // GET
    List<DonationResponseDto> getDonationsByMonth(int year, int month);

    // GET
    List<DonationResponseDto> getDonationsByYear(int year);

    // UPDATE
    DonationResponseDto updateVisibilityDonation(UUID publicId);

    // UPDATE
    DonationResponseDto updateClosureStatusDonation(UUID publicId);

    // UPDATE
    DonationResponseDto updateDonation(UUID publicId, DonationRequestDto dto, MultipartFile photoFile) throws IOException;

    // DELETE
    void deleteDonation(UUID publicId);
}
