package busness.ecommerce.controller;

import busness.ecommerce.config.JwtUtils;
import busness.ecommerce.dto.AuthResponse;
import busness.ecommerce.dto.LoginRequest;
import busness.ecommerce.dto.LoginResponse;
import busness.ecommerce.dto.RegisterRequest;
import busness.ecommerce.entity.UserProfile;
import busness.ecommerce.entity.Role;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.RoleName;
import busness.ecommerce.repository.ClientRepository;
import busness.ecommerce.repository.RoleRepository;
import busness.ecommerce.repository.UserRepository;
import busness.ecommerce.services.CustomUserDetails;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping(value="/api/v1/auth")
@RequiredArgsConstructor
@Slf4j
@Transactional
public class AuthRestController {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtUtils jwtUtils;
    private final ClientRepository clientRepository;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest dto) {

        Role roleUser = roleRepository.findByName(RoleName.ROLE_CLIENT)
                .orElseGet(() -> roleRepository.save(
                        new Role(null, RoleName.ROLE_CLIENT)));

        User user = new User();
        user.setUsername(dto.getUsername());
        user.setEmail(dto.getEmail());
        user.setPassword(passwordEncoder.encode(dto.getPassword()));
        user.getRoles().add(roleUser);

        userRepository.save(user);

        // création automatique du profil
        UserProfile profile = UserProfile.builder()
                .user(user)
                .build();

        return ResponseEntity.ok(clientRepository.save(profile));
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

        return ResponseEntity.ok(
                LoginResponse.builder()
                        .token(token)
                        .type("Bearer")
                        .username(userDetails.getUsername())
                        .roles(
                                userDetails.getAuthorities()
                                        .stream()
                                        .map(GrantedAuthority::getAuthority)
                                        .toList()
                        )
                        .build()
        );
    }

    @GetMapping("/me")
    public AuthResponse me(Authentication authentication) {

        CustomUserDetails userDetails =
                (CustomUserDetails) authentication.getPrincipal();

        return new AuthResponse(
                userDetails.getUser().getId(),
                userDetails.getUsername(),
                userDetails.getUser().getEmail(),
                userDetails.getAuthorities()
                        .stream()
                        .map(GrantedAuthority::getAuthority)
                        .toList()
        );
    }
}

