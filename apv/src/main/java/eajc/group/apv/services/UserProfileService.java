package eajc.group.apv.services;

import eajc.group.apv.dto.*;
import eajc.group.apv.enums.Reason;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public interface UserProfileService {
    UserProfileResponseDto createProfile(UserProfileRequestDto profileDto, MultipartFile photoFile) throws IOException ;

    // READ
    List<UserProfileResponseDto> getAllProfiles();

    // GET
    UserProfileResponseDto getProfileByPublicId(UUID publicId);

    // GET
    UserProfileResponseDto getProfileByUser(UUID publicId);

    // GET
    List<UserProfileResponseDto> getTodayRegistrations();

    // GET
    List<GenderCountDto> countProfilesByGender();

    // GET
    List<UserProfileResponseDto> getProfilesByReasonRemovalNot();

    // UPDATE
    UserProfileResponseDto updateReasonRemoval(UUID publicId, UserProfileReasonRemovalDto dto);

    // PATCH
    UserProfileResponseDto updateProfile(UUID publicId, UserProfileRequestDto dto);

    // PATCH
    UserProfileResponseDto updatePhotoProfile(UUID publicId, MultipartFile photoFile) throws IOException;

    // DELETE
    void deleteProfile(UUID publicId);
}
