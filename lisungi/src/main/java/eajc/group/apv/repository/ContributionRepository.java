package eajc.group.apv.repository;

import eajc.group.apv.entity.Contribution;
import eajc.group.apv.entity.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface ContributionRepository extends JpaRepository<Contribution, Long> {
    Optional<Contribution> findByPublicId(UUID publicId);
    List<Contribution> findByEventId(Long eventId);
    List<Contribution> findByContributedId(Long eventId);
    boolean existsByContributedIdAndEventId(Long contributedId, Long eventTypeId);
    boolean existsByContributedIdAndEventIdAndPublicIdNot(Long contributedId, Long eventId, UUID publicId);

    // Grouper les contributions par contributeur
    @Query("""
        SELECT c.contributed.id, c.contributed.publicId, c.contributed.profile.lastName, c.contributed.profile.firstName, COUNT(c.id)
        FROM Contribution c
        GROUP BY c.contributed.id, c.contributed.publicId, c.contributed.profile.lastName, c.contributed.profile.firstName
    """)
    List<Object[]> countContributionsByContributed();

    @Query("""
        SELECT 
            e.eventType.id,
            e.eventType.publicId,
            e.eventType.name,
            COUNT(DISTINCT e.id)
        FROM Event e
        JOIN e.contributions c
        GROUP BY 
            e.eventType.id,
            e.eventType.publicId,
            e.eventType.name
    """)
    List<Object[]> countEventByEventTypeWithContribution();

    @Query("""
        SELECT
            c.event.id,
            c.event.publicId,
            c.event.name,
            c.event.closure_status,
            c.event.mount,
            c.event.amountTotal,
            COUNT(c)
        FROM Contribution c
        WHERE c.event.eventType.publicId = :publicId
        GROUP BY c.event.id, c.event.publicId, c.event.name, c.event.closure_status, c.event.mount, c.event.amountTotal
    """)
    List<Object[]> countContributionsByEventAndEventType(
            @Param("publicId") UUID eventTypePublicId
    );

    // Calucler la ssomme des contribution d'un évènement
    @Query("""
        SELECT COALESCE(SUM(c.amount), 0)
        FROM Contribution c
        WHERE c.event.id = :eventId
    """)
    BigDecimal sumContributionsByEvent(@Param("eventId") Long eventId);

    @Query("""
        SELECT et.id, et.publicId, et.name, COUNT(c.id)
        FROM EventType et
        LEFT JOIN et.events e
        LEFT JOIN e.contributions c
        GROUP BY et.id, et.publicId, et.name
        ORDER BY COUNT(c.id) DESC
    """)
    List<Object[]> countContributionsByEventType();
}
