package eajc.group.apv.repository;

import eajc.group.apv.dto.EventCountByYearDto;
import eajc.group.apv.entity.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface EventRepository extends JpaRepository<Event, Long> {

    Optional<Event> findByPublicId(UUID publicId);

    List<Event> findByEventTypeId(Long eventTypeId);

    boolean existsByUserIdAndEventTypeId(Long userId, Long eventTypeId);

    boolean existsByUserIdAndEventTypeIdAndPublicIdNot(Long userId, Long eventTypeId, UUID publicId);

    List<Event> findByEventDateBetween(
            LocalDate startDate,
            LocalDate endDate
    );

    @Query("""
            SELECT YEAR(e.eventDate), COUNT(e)
            FROM Event e
            GROUP BY YEAR(e.eventDate)
            ORDER BY YEAR(e.eventDate)
        """)
    List<Object[]> countEventsByYear();

    @Query("""
        SELECT e.eventType.id, e.eventType.publicId, e.eventType.name, COUNT(e)
        FROM Event e
        GROUP BY e.eventType.id, e.eventType.publicId, e.eventType.name
    """)
    List<Object[]> countEventsByEventType();
}
