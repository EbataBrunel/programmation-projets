package busness.ecommerce.mapper;

import busness.ecommerce.dto.UserProfileRequestDto;
import busness.ecommerce.dto.UserProfileResponseDto;
import busness.ecommerce.entity.UserProfile;
import busness.ecommerce.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserProfileMapper {
    public UserProfile toEntity(UserProfileRequestDto dto, User user, String filename) {
        return UserProfile.builder()
                .firstName(dto.getFirstName())
                .lastName(dto.getLastName())
                .phone(dto.getPhone())
                .address(dto.getAddress())
                .country(dto.getCountry())
                .city(dto.getCity())
                .borough(dto.getBorough())
                .photo(filename)
                .user(user)
                .build();
    }

    public UserProfileResponseDto toDto(UserProfile client) {
        return UserProfileResponseDto.builder()
                .id(client.getId())
                .firstName(client.getFirstName())
                .lastName(client.getLastName())
                .phone(client.getPhone())
                .address(client.getAddress())
                .userId(client.getUser().getId())
                .country(client.getCountry())
                .city(client.getCity())
                .borough(client.getBorough())
                .photo(client.getPhoto())
                .build();
    }
}
