package eajc.group.apv.repository;

import eajc.group.apv.entity.News;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface NewsRepository extends JpaRepository<News, Long> {
    Optional<News> findByPublicId(UUID publicId);
    boolean existsByTitleIgnoreCase(String title);
    boolean existsByTitleIgnoreCaseAndPublicIdNot(String title, UUID publicId);
}
