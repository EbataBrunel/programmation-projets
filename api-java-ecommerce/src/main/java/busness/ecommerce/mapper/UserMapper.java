package busness.ecommerce.mapper;

import busness.ecommerce.dto.*;
import busness.ecommerce.entity.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
public class UserMapper {

    private final RoleMapper roleMapper;
    /*
    public User toEntity (RegisterRequest dto){
        return User.builder()
                .username(dto.getUsername())
                .email(dto.getEmail())
                .password(dto.getPassword())
                .enabled(true)
                .build();
    }*/

    public UserResponseDto toDto(User user) {
        return UserResponseDto.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .enabled(user.isEnabled())
                .roles(
                        user.getRoles() == null
                                ? null
                                : user.getRoles()
                                    .stream()
                                    .map(role -> RoleResponseDto.builder()
                                            .id(role.getId())
                                            .name(role.getName())
                                            .build())
                                    .toList()
                )
                .build();
    }

}
