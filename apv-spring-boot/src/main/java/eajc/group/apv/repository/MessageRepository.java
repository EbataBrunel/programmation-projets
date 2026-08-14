package eajc.group.apv.repository;

import eajc.group.apv.entity.Message;
import eajc.group.apv.enums.MessageStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface MessageRepository extends JpaRepository<Message, Long> {
    Optional<Message> findByPublicId(UUID publicId);
    long countByReceiverIdAndStatus(Long receiverId, MessageStatus status);

    @Query("""
            SELECT m
            FROM Message m
            WHERE
                (m.sender.id=:user1 AND m.receiver.id=:user2)
             OR (m.sender.id=:user2 AND m.receiver.id=:user1)
            ORDER BY m.sentAt ASC
            """)
    List<Message> findConversation(@Param("user1") Long user1,
                                   @Param("user2") Long user2);

    @Query("""
        SELECT m
        FROM Message m
        WHERE m.sender.id = :currentUserId
           OR m.receiver.id = :currentUserId
        ORDER BY m.sentAt DESC
    """)
    List<Message> findAllConversations(Long currentUserId);

}
