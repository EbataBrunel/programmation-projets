package busness.ecommerce.services;



import busness.ecommerce.dto.SettingRequestDto;
import busness.ecommerce.dto.SettingResponseDto;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

public interface SettingService {
    // CREATE
    SettingResponseDto createSetting(SettingRequestDto dto, MultipartFile logoFile) throws IOException;

    // READ
    List<SettingResponseDto> getAllSetting();

    // GET
    SettingResponseDto getSettingById(Long id);

    // GET
    SettingResponseDto getLastSetting();

    // UPDATE
    SettingResponseDto updateSetting(Long id, SettingRequestDto dto, MultipartFile logoFile) throws IOException;

    // DELETE
    void deleteSetting(Long id);
}
