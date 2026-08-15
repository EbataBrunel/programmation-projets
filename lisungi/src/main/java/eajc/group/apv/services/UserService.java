package eajc.group.apv.services;

import eajc.group.apv.dto.UserResponseDto;
import eajc.group.apv.entity.User;

import java.util.List;
import java.util.UUID;

public interface UserService {
    public UserResponseDto addRoleToUser(UUID userId, String roleName);
    UserResponseDto removeRoleToUser(UUID userId, String roleName);
    public List<UserResponseDto> findAllUsers();
    public UserResponseDto findUser(UUID userId);
    public UserResponseDto findUserById(Long userId);
    public void deleteUser(UUID publicId);
    public User getCurrentUser();
    public UserResponseDto getUserByUsername(String username);
}
