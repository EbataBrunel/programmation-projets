package busness.ecommerce.services;

import busness.ecommerce.dto.UserResponseDto;
import busness.ecommerce.entity.Role;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.RoleName;
import busness.ecommerce.mapper.UserMapper;
import busness.ecommerce.repository.RoleRepository;
import busness.ecommerce.repository.UserRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService{

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final UserMapper userMapper;

    @Override
    public UserResponseDto addRoleToUser(Long userId, RoleName roleName) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Role role = roleRepository.findByName(roleName)
                .orElseThrow(() -> new RuntimeException("Role not found"));

        user.getRoles().add(role);

        return userMapper.toDto(userRepository.save(user));
    }

    @Override
    public List<UserResponseDto> findAllUsers() {
        return userRepository.findAll()
                .stream()
                .map(userMapper::toDto)
                .toList();
    }

    @Override
    public UserResponseDto findUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return userMapper.toDto(user);
    }

    @Override
    @Transactional
    public void deleteUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));

        user.getRoles().clear(); // obligatoire
        userRepository.save(user);
        userRepository.delete(user);
    }

    @Override
    public User getCurrentUser() {
        Authentication authentication =
                SecurityContextHolder.getContext().getAuthentication();

        if (authentication == null ||
                !authentication.isAuthenticated() ||
                authentication.getPrincipal().equals("anonymousUser")) {

            throw new RuntimeException("Utilisateur non authentifié");
        }

        String username;

        // Cas standard Spring Security
        if (authentication.getPrincipal() instanceof UserDetails userDetails) {
            username = userDetails.getUsername();
        }
        // Cas JWT custom
        else if (authentication.getPrincipal() instanceof String) {
            username = (String) authentication.getPrincipal();
        }
        else {
            throw new RuntimeException("Impossible de récupérer l'utilisateur");
        }

        return userRepository.findByUsername(username);
    }

    @Override
    public UserResponseDto getUserByUsername(String username) {
        return userMapper.toDto(userRepository.findByUsername(username));
    }

}
