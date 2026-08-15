package eajc.group.apv.mapper;

import eajc.group.apv.dto.UserProfileRequestDto;
import eajc.group.apv.dto.UserProfileResponseDto;
import eajc.group.apv.entity.UserProfile;
import eajc.group.apv.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserProfileMapper {

    public UserProfile toEntity(UserProfileRequestDto dto, User user, String filename) {

        UserProfile profile = new UserProfile();

        profile.setFirstName(dto.getFirstName());
        profile.setLastName(dto.getLastName());
        profile.setGender(dto.getGender());
        profile.setPhone(dto.getPhone());
        profile.setAddress(dto.getAddress());
        profile.setCountry(dto.getCountry());
        profile.setCity(dto.getCity());
        profile.setBorough(dto.getBorough());
        profile.setProfession(dto.getProfession());
        profile.setPhoto(filename);
        profile.setUser(user);

        return profile;
    }

    public UserProfileResponseDto toDto(UserProfile profile) {

        UserProfileResponseDto dto = new UserProfileResponseDto();

        dto.setPublicId(profile.getPublicId());
        dto.setFirstName(profile.getFirstName());
        dto.setGender(
                profile.getGender() != null
                        ? profile.getGender().name()
                        : null
        );
        dto.setLastName(profile.getLastName());
        dto.setPhone(profile.getPhone());
        dto.setAddress(profile.getAddress());
        dto.setUserId(profile.getUser().getId());
        dto.setCountry(profile.getCountry());
        dto.setCity(profile.getCity());
        dto.setBorough(profile.getBorough());
        dto.setProfession(profile.getProfession());
        dto.setPhoto(profile.getPhoto());
        dto.setRegistrationDate(profile.getRegistrationDate());
        dto.setReasonRemoval(
               profile.getReasonRemoval() != null
                        ? profile.getReasonRemoval().getLabel()
                        : null
        );
        dto.setUserName(profile.getUser().getUsername());
        dto.setUserEmail(profile.getUser().getEmail());

        return dto;
    }
}