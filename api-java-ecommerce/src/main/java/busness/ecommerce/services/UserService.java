package busness.ecommerce.services;

import busness.ecommerce.dto.UserResponseDto;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.RoleName;

import java.util.List;

public interface UserService {
    public UserResponseDto addRoleToUser(Long userId, RoleName roleName);
    public List<UserResponseDto> findAllUsers();
    public UserResponseDto findUser(Long userId);
    public void deleteUser(Long id);
    public User getCurrentUser();
    public UserResponseDto getUserByUsername(String username);
}
