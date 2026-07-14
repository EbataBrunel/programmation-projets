package busness.ecommerce.mapper;

import busness.ecommerce.dto.ContactRequestDto;
import busness.ecommerce.dto.ContactResponseDto;
import busness.ecommerce.entity.Contact;
import org.springframework.stereotype.Component;

@Component
public class ContactMapper {
    public Contact toEntity(ContactRequestDto dto){
        return Contact.builder()
                .lastname(dto.getLastname())
                .firstname(dto.getFirstname())
                .email(dto.getEmail())
                .subject(dto.getSubject())
                .message(dto.getMessage())
                .status(0)
                .build();
    }

    public ContactResponseDto toDto(Contact contact){
        return ContactResponseDto.builder()
                .id(contact.getId())
                .lastname(contact.getLastname())
                .firstname(contact.getFirstname())
                .email(contact.getEmail())
                .subject(contact.getSubject())
                .message(contact.getMessage())
                .status(contact.getStatus())
                .createdAt(contact.getCreatedAt())
                .build();
    }
}
