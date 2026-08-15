package eajc.group.apv.repository;

import eajc.group.apv.entity.Regulation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface RegulationRepository extends JpaRepository<Regulation, Long> {
    Optional<Regulation> findByPublicId(UUID publicId);
    boolean existsByNameIgnoreCase(String name);
    boolean existsByNameIgnoreCaseAndPublicIdNot(String name, UUID publicId);
}
