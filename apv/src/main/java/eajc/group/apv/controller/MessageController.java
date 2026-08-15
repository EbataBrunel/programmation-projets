package eajc.group.apv.controller;

import eajc.group.apv.dto.ConversationDto;
import eajc.group.apv.dto.MessageRequestDto;
import eajc.group.apv.dto.MessageResponseDto;
import eajc.group.apv.services.CustomUserDetails;
import eajc.group.apv.services.MessageService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/messages")
public class MessageController {
    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }


    @PostMapping
    public ResponseEntity<MessageResponseDto> send(
            @RequestBody @Valid MessageRequestDto dto) {

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(messageService.createMessage(dto));
    }

    @GetMapping
    public ResponseEntity<List<MessageResponseDto>> all() {
        return ResponseEntity.ok(messageService.getAllMessages());
    }

    @GetMapping("/{publicId}")
    public ResponseEntity<MessageResponseDto> one(
            @PathVariable UUID publicId) {

        return ResponseEntity.ok(
                messageService.getMessageByPublicId(publicId)
        );
    }

    @GetMapping("/conversation")
    public ResponseEntity<List<MessageResponseDto>> conversation(
            @RequestParam Long otherUserId,
            Authentication authentication) {

        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(
                messageService.getConversation(user.getUser().getId(), otherUserId)
        );
    }

    @GetMapping("/conversations")
    public ResponseEntity<List<ConversationDto>> conversations(
            Authentication authentication) {

        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();


        return ResponseEntity.ok(
                messageService.getConversations(user.getUser().getId())
        );
    }

    @PatchMapping("/read")
    public ResponseEntity<Void> markAsRead(
            @RequestParam Long otherUserId,
            Authentication authentication) {

        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();


        messageService.markConversationAsRead(
                user.getUser().getId(),
                otherUserId
        );

        return ResponseEntity.noContent().build();
    }

    @GetMapping("/unread")
    public ResponseEntity<Long> unread(
            Authentication authentication) {

        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(
                messageService.countUnreadMessages(user.getUser().getId())
        );
    }

    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId) {

        messageService.deleteMessage(publicId);

        return ResponseEntity.noContent().build();
    }
}
