package busness.ecommerce.services;

import busness.ecommerce.dto.SettingRequestDto;
import busness.ecommerce.dto.UserProfileRequestDto;
import busness.ecommerce.dto.UserProfileResponseDto;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

public interface UserProfileService {
    UserProfileResponseDto createProfile(UserProfileRequestDto clientDto, MultipartFile photoFile) throws IOException ;

    // READ
    List<UserProfileResponseDto> getAllProfiles();

    // GET
    UserProfileResponseDto getProfileById(Long id);

    // GET
    UserProfileResponseDto getProfileByUser(Long id);

    // PATCH
    UserProfileResponseDto updateProfile(Long id, UserProfileRequestDto dto);

    // PATCH
    UserProfileResponseDto updatePhotoProfile(Long id, MultipartFile photoFile) throws IOException;

    // DELETE
    void deleteProfile(Long id);
}
