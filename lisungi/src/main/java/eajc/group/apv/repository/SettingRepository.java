package eajc.group.apv.repository;

import eajc.group.apv.entity.Setting;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface SettingRepository extends JpaRepository<Setting, Long> {
    Optional<Setting> findByPublicId(UUID publicId);
    Optional<Setting> findTopByOrderByIdDesc();
    Optional<Setting> findFirstByOrderByIdAsc();
}
