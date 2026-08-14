package eajc.group.apv.services;

import eajc.group.apv.dto.BeneficiaryRequestDto;
import eajc.group.apv.dto.BeneficiaryResponseDto;

import java.util.List;
import java.util.UUID;

public interface BeneficiaryService {
    // CREATE
    BeneficiaryResponseDto createBeneficiary(BeneficiaryRequestDto dto);

    // READ
    List<BeneficiaryResponseDto> getAllBeneficiaries();

    // GET
    BeneficiaryResponseDto getBeneficiaryByPublicId(UUID publicId);

    // UPDATE
    BeneficiaryResponseDto updateBeneficiary(UUID publicId, BeneficiaryRequestDto dto);

    // DELETE
    void deleteBeneficiary(UUID publicId);
}
