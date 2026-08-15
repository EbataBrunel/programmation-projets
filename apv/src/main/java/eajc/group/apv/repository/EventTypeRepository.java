package eajc.group.apv.repository;

import eajc.group.apv.entity.EventType;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface EventTypeRepository extends JpaRepository<EventType, Long> {
    Optional<EventType> findByPublicId(UUID publicId);
    boolean existsByNameIgnoreCase(String name);
    boolean existsByNameIgnoreCaseAndPublicIdNot(String name, UUID publicId);
}
