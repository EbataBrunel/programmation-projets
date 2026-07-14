package busness.ecommerce.config;

import busness.ecommerce.entity.Role;
import busness.ecommerce.entity.Setting;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.RoleName;
import busness.ecommerce.repository.RoleRepository;
import busness.ecommerce.repository.SettingRepository;
import busness.ecommerce.repository.UserRepository;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
public class DataInitializer {

    private final RoleRepository roleRepository;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final SettingRepository settingRepository;

    @PostConstruct
    public void init() {

        Role adminRole = roleRepository.findByName(RoleName.ROLE_ADMIN)
                .orElseGet(() ->
                        roleRepository.save(new Role(null, RoleName.ROLE_ADMIN))
                );

        Role sellerRole = roleRepository.findByName(RoleName.ROLE_SELLER)
                .orElseGet(() ->
                        roleRepository.save(new Role(null, RoleName.ROLE_SELLER))
                );

        Role customerRole = roleRepository.findByName(RoleName.ROLE_CLIENT)
                .orElseGet(() ->
                        roleRepository.save(new Role(null, RoleName.ROLE_CLIENT))
                );

        Role userRole = roleRepository.findByName(RoleName.ROLE_USER)
                .orElseGet(() ->
                        roleRepository.save(new Role(null, RoleName.ROLE_USER))
                );

        if (!userRepository.existsByUsername("admin")) {

            User admin = new User();
            admin.setUsername("admin");
            admin.setEmail("admin@gmail.com");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.getRoles().add(adminRole);
            admin.getRoles().add(userRole);
            admin.getRoles().add(sellerRole);
            admin.getRoles().add(customerRole);

            userRepository.save(admin);
        }

        // ===== DEFAULT SETTING =====
        if (settingRepository.findAll().isEmpty()) {

            Setting defaultSetting = Setting.builder()
                    .nameApp("EAJC Ecommerce")
                    .nameDev("EBATA-ATIPO Brunel")
                    .version("1.0.0")
                    .theme("light")
                    .textColor("#000000")
                    .currency("USD")
                    .address("5 rue de Tours")
                    .email("contact@ecommerce.com")
                    .phone("+33 0000000")
                    .logo("default-logo.png")
                    .width(200)
                    .height(100)
                    .build();

            settingRepository.save(defaultSetting);
        }

    }
}
