package eajc.group.apv.services;



import eajc.group.apv.dto.SettingRequestDto;
import eajc.group.apv.dto.SettingResponseDto;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

public interface SettingService {
    // CREATE
    SettingResponseDto createSetting(SettingRequestDto dto, MultipartFile logoFile) throws IOException;

    // READ
    List<SettingResponseDto> getAllSetting();

    // GET
    SettingResponseDto getSettingByPublicId(UUID publicId);

    // GET
    SettingResponseDto getLastSetting();

    // UPDATE
    SettingResponseDto updateSetting(UUID publicId, SettingRequestDto dto, MultipartFile logoFile) throws IOException;

    // DELETE
    void deleteSetting(UUID publicId);
}
