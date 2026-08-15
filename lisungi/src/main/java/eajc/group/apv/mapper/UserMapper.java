package eajc.group.apv.mapper;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.User;
import org.springframework.stereotype.Component;

import java.util.List;

@Component

public class UserMapper {

    private final RoleMapper roleMapper;
    private final UserProfileMapper userProfileMapper;

    public UserMapper(RoleMapper roleMapper, UserProfileMapper userProfileMapper) {
        this.roleMapper = roleMapper;
        this.userProfileMapper = userProfileMapper;
    }

    public UserResponseDto toDto(User user) {

        UserResponseDto dto = new UserResponseDto();

        dto.setId(user.getId());
        dto.setPublicId(user.getPublicId());
        dto.setUsername(user.getUsername());
        dto.setEmail(user.getEmail());
        dto.setEnabled(user.isEnabled());

        dto.setUserProfile(userProfileMapper.toDto(user.getProfile()));

        dto.setRoles(
                user.getRoles() == null
                        ? null
                        : user.getRoles()
                        .stream()
                        .map(roleMapper::toDto)
                        .toList()
        );

        return dto;
    }

}
