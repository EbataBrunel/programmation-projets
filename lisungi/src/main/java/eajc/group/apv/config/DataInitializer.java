package eajc.group.apv.config;

import eajc.group.apv.entity.Role;
import eajc.group.apv.entity.Setting;
import eajc.group.apv.entity.User;
import eajc.group.apv.repository.RoleRepository;
import eajc.group.apv.repository.SettingRepository;
import eajc.group.apv.repository.UserRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer {

    private final RoleRepository roleRepository;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final SettingRepository settingRepository;

    // Remplace @RequiredArgsConstructor
    public DataInitializer(RoleRepository roleRepository,
                           UserRepository userRepository,
                           PasswordEncoder passwordEncoder,
                           SettingRepository settingRepository) {
        this.roleRepository = roleRepository;
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.settingRepository = settingRepository;
    }

    private Role createRoleIfNotExists(String name) {

        return roleRepository.findByName(name)
                .orElseGet(() -> {
                    Role role = new Role();
                    role.setName(name);
                    return roleRepository.save(role);
                });
    }

    @PostConstruct
    public void init() {

        Role adminRole = createRoleIfNotExists("ROLE_ADMIN");
        Role supadminRole = createRoleIfNotExists("ROLE_SUPADMIN");
        Role customerRole = createRoleIfNotExists("ROLE_CUSTOMER");

        if (!userRepository.existsByUsername("admin")) {

            User admin = new User();

            admin.setUsername("admin");
            admin.setEmail("admin@gmail.com");
            admin.setPassword(passwordEncoder.encode("admin123"));

            admin.getRoles().add(adminRole);
            admin.getRoles().add(supadminRole);
            admin.getRoles().add(customerRole);

            userRepository.save(admin);
        }


        // ===== DEFAULT SETTING =====
        if (settingRepository.findAll().isEmpty()) {

            Setting defaultSetting = new Setting();

            defaultSetting.setNameApp("APV");
            defaultSetting.setNameDev("EBATA-ATIPO Brunel");
            defaultSetting.setVersion("1.0.0");
            defaultSetting.setTheme("bg-maroon");
            defaultSetting.setBodyTheme("bg-maroon");
            defaultSetting.setTextColor("text-white");
            defaultSetting.setCurrency("USD");
            defaultSetting.setAddress("5 rue de Tours");
            defaultSetting.setEmail("contact@ecommerce.com");
            defaultSetting.setPhone("+33 0000000");
            defaultSetting.setLogo("default-logo.png");
            defaultSetting.setWidth(200);
            defaultSetting.setHeight(100);

            settingRepository.save(defaultSetting);
        }
    }
}