package eajc.group.apv.repository;

import eajc.group.apv.entity.Contact;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface ContactRepository extends JpaRepository<Contact, Long> {
    Optional<Contact> findByPublicId(UUID publicId);

    List<Contact> findAllByOrderByCreatedAtDesc();

    @Query("""
    SELECT COUNT(c)
        FROM Contact c
        WHERE c.status = :status
    """)
    int countContactByStatus(
            @Param("status") int status
    );

    @Modifying
    @Query("UPDATE Contact c SET c.status = 1 WHERE c.status = 0")
    int updateAllStatus0To1();
}
