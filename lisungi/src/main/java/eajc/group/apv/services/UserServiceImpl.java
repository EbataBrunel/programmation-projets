package eajc.group.apv.services;

import eajc.group.apv.dto.UserResponseDto;
import eajc.group.apv.entity.Role;
import eajc.group.apv.entity.User;
import eajc.group.apv.mapper.UserMapper;
import eajc.group.apv.repository.RoleRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class UserServiceImpl implements UserService{

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final UserMapper userMapper;

    public UserServiceImpl(UserRepository userRepository, RoleRepository roleRepository, UserMapper userMapper) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.userMapper = userMapper;
    }

    @Override
    public UserResponseDto addRoleToUser(UUID userId, String roleName) {
        User user = userRepository.findByPublicId(userId)
                .orElseThrow(() -> new RuntimeException("Rôle introuvable"));

        Role role = roleRepository.findByName(roleName)
                .orElseThrow(() -> new RuntimeException("Rôle introuvable"));

        user.getRoles().add(role);

        return userMapper.toDto(userRepository.save(user));
    }

    @Override
    @Transactional
    public UserResponseDto removeRoleToUser(UUID userId, String roleName) {

        User user = userRepository.findByPublicId(userId)
                .orElseThrow(() ->
                        new RuntimeException("Utilisateur introuvable"));

        Role role = roleRepository.findByName(roleName)
                .orElseThrow(() ->
                        new RuntimeException("Rôle introuvable"));

        user.getRoles().remove(role);

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
    public UserResponseDto findUser(UUID userId) {
        User user = userRepository.findByPublicId(userId)
                .orElseThrow(() -> new RuntimeException("Utilisateur introuvable"));
        return userMapper.toDto(user);
    }

    @Override
    public UserResponseDto findUserById(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("Utilisateur introuvable"));
        return userMapper.toDto(user);
    }

    @Override
    @Transactional
    public void deleteUser(UUID publicId) {
        User user = userRepository.findByPublicId(publicId)
                .orElseThrow(() -> new RuntimeException("Utilisateur introuvable"));

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

        User user = userRepository.findByUsername(username)
            .orElseThrow(() -> new RuntimeException("Utilisateur introuvable"));
        return user;
    }

    @Override
    public UserResponseDto getUserByUsername(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("Utilisateur introuvable"));
        return userMapper.toDto(user);
    }

}
