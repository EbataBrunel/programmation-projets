package eajc.group.apv.controller;

import eajc.group.apv.config.JwtUtils;
import eajc.group.apv.dto.*;
import eajc.group.apv.entity.PasswordResetToken;
import eajc.group.apv.entity.UserProfile;
import eajc.group.apv.entity.Role;
import eajc.group.apv.entity.User;
import eajc.group.apv.repository.UserProfileRepository;
import eajc.group.apv.repository.RoleRepository;
import eajc.group.apv.repository.UserRepository;
import eajc.group.apv.services.CustomUserDetails;
import eajc.group.apv.services.PasswordResetService;
import jakarta.validation.Valid;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/auth")
@Transactional
public class AuthRestController {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtUtils jwtUtils;
    private final UserProfileRepository userProfileRepository;
    private final PasswordResetService passwordResetService;

    public AuthRestController(UserRepository userRepository, RoleRepository roleRepository, PasswordEncoder passwordEncoder, AuthenticationManager authenticationManager, JwtUtils jwtUtils, UserProfileRepository userProfileRepository, PasswordResetService passwordResetService) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtUtils = jwtUtils;
        this.userProfileRepository = userProfileRepository;
        this.passwordResetService = passwordResetService;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest dto) {

        Role roleUser = roleRepository.findByName("ROLE_CUSTOMER")
                .orElseGet(() -> {
                    Role role = new Role();
                    role.setName("ROLE_CUSTOMER");
                    return roleRepository.save(role);
                });

        User user = new User();
        user.setUsername(dto.getUsername());
        user.setEmail(dto.getEmail());
        user.setPassword(passwordEncoder.encode(dto.getPassword()));
        user.getRoles().add(roleUser);

        userRepository.save(user);

        // création automatique du profil
        UserProfile profile = new UserProfile();
        profile.setUser(user);

        return ResponseEntity.ok(userProfileRepository.save(profile));
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        Authentication authentication =
                authenticationManager.authenticate(
                        new UsernamePasswordAuthenticationToken(
                                request.getUsername(),
                                request.getPassword()
                        )
                );

        CustomUserDetails userDetails =
                (CustomUserDetails) authentication.getPrincipal();

        String token = jwtUtils.generateToken(userDetails);

        LoginResponse response = new LoginResponse();
        response.setToken(token);
        response.setType("Bearer");
        response.setUsername(userDetails.getUsername());
        response.setRoles(
                userDetails.getAuthorities()
                            .stream()
                            .map(GrantedAuthority::getAuthority)
                            .toList()
        );

        return ResponseEntity.ok(response);
    }

    @GetMapping("/me")
    public AuthResponse me(Authentication authentication) {

        CustomUserDetails userDetails =
                (CustomUserDetails) authentication.getPrincipal();

        return new AuthResponse(
                userDetails.getUser().getId(),
                userDetails.getUser().getPublicId(),
                userDetails.getUsername(),
                userDetails.getUser().getEmail(),
                userDetails.getAuthorities()
                        .stream()
                        .map(GrantedAuthority::getAuthority)
                        .toList()
        );
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<Void> forgotPassword(
            @Valid @RequestBody ForgotPasswordRequest request){

        passwordResetService.forgotPassword(request);

        return ResponseEntity.ok().build();
    }

    @PostMapping("/reset-password")
    public ResponseEntity<Void> resetPassword(
            @Valid @RequestBody ResetPasswordRequest request) {

        passwordResetService.resetPassword(request);

        return ResponseEntity.ok().build();
    }

    @PutMapping("/change-password")
    public ResponseEntity<?> changePassword(
            Authentication authentication,
            @RequestBody ChangePasswordRequest request) {

        passwordResetService.changePassword(authentication.getName(), request);

        return ResponseEntity.ok("Mot de passe modifié avec succès");
    }
}

