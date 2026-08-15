package eajc.group.apv.repository;

import eajc.group.apv.entity.User;
import eajc.group.apv.entity.View;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface ViewRepository extends JpaRepository<View, Long> {
    List<View> findByAdminIdAndStatusFalse(Long adminId);
    Optional<View> findByPublicId(UUID publicId);

    @Query("""
        SELECT u
        FROM User u
        WHERE u.id <> :adminId
        AND NOT EXISTS (
            SELECT v.id
            FROM View v
            WHERE v.admin.id = :adminId
            AND v.user.id = u.id
        )
    """)
    List<User> findUsersWithoutViewForAdmin(@Param("adminId") Long adminId);

    @Query("""
    SELECT COUNT(u)
    FROM User u
    WHERE u.id <> :adminId
    AND NOT EXISTS (
        SELECT v.id FROM View v
        WHERE v.admin.id = :adminId
        AND v.user.id = u.id
    )
""")
    int countUsersNotViewWithAdmin(@Param("adminId") Long adminId);

    // Modifie à true toutes les views de l'admin
    @Modifying
        @Query("""
        UPDATE View v
        SET v.status = true
        WHERE v.admin.id = :adminId
        AND v.status = false
    """)
        int markAllViewsAsViewed(@Param("adminId") Long adminId);
}
