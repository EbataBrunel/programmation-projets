package eajc.group.apv.services;

import eajc.group.apv.dto.RegulationRequestDto;
import eajc.group.apv.dto.RegulationResponseDto;

import java.util.List;
import java.util.UUID;

public interface RegulationService {

    // CREATE
    public RegulationResponseDto createRegulation(RegulationRequestDto dto, Long userId);

    // READ
    List<RegulationResponseDto> getAllRegulations();

    // GET
    RegulationResponseDto getRegulationByPublicId(UUID publicId);

    // UPDATE
    RegulationResponseDto updateRegulation(UUID publicId, RegulationRequestDto dto, Long userId);

    // DELETE
    void deleteRegulation(UUID publicId);

}
