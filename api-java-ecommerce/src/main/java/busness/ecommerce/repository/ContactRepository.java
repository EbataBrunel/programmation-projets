package busness.ecommerce.repository;

import busness.ecommerce.entity.Contact;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ContactRepository extends JpaRepository<Contact, Long> {
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
