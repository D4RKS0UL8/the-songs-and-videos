# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING

import os, random, json
import bascenev1 as bs
import bauiv1 as bui
import babase as ba
from bauiv1 import SpecialChar, charstr
from bascenev1._activity import Activity
from bascenev1lib.actor.bomb import Bomb
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.mainmenu import MainMenuActivity
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spazfactory import SpazFactory

import bascenev1lib.actor.popuptext as ptext
import bascenev1lib.actor.text as text
import bascenev1lib.actor.image as image
import bascenev1lib.actor.spaz as spaz

if TYPE_CHECKING:
    from typing import Sequence, Any, Callable

class Lang:
    def __init__(self,
                 text: str,
                 subs: list[str] = 'none'):
        
        icons = [bui.charstr(bui.SpecialChar.CROWN),
                 bui.charstr(bui.SpecialChar.LOGO)]
 
        lang = bs.app.lang.language
        setphrases = {
            "Installing":
                {"Spanish": f"Instalando <{__name__}>",
                 "English": f"Installing <{__name__}>",
                 "Portuguese": f"Instalando <{__name__}>"},
            "Installed":
                {"Spanish": f"¡<{__name__}> Se instaló correctamente!",
                 "English": f"<{__name__}> Installed successfully!",
                 "Portuguese": f"<{__name__}> Instalado com sucesso!"},
            "Make Sys":
                {"Spanish": "Se creó la carpeta sys",
                 "English": "Sys folder created",
                 "Portuguese": "Pasta sys criada"},
            "Restart Msg":
                {"Spanish": "Reiniciando...",
                 "English": "Rebooting...",
                 "Portuguese": "Reinício..."},
            "EJ":
                {"Spanish": f"Datos incompletos \n Ejemplo: {subs}",
                 "English": f"Incomplete data \n Example: {subs}",
                 "Portuguese": f"Dados incompletos \n Exemplo: {subs}"},
            "EX":
                {"Spanish": f"Ejemplo: {subs}",
                 "English": f"Example: {subs}",
                 "Portuguese": f"Exemplo: {subs}"},
            "Error Entering Client ID":
                {"Spanish": f"'{subs[0]}' no es válido. \n Ingresa números \n Ejemplo: {subs[1]}",
                 "English": f"'{subs[0]}' is invalid. \n Enter numbers \n Example: {subs[1]}",
                 "Portuguese": f"'{subs[0]}' é inválido. \n Digite os números \n Exemplo: {subs[1]}"},
            "Error Entering Player ID":
                {"Spanish": f"'{subs}' no es válido. \n Ingresa el ID del jugador. consulta el comando '-i'",
                 "English": f"'{subs}' no es válido. \n Add the player ID. use the '-i' command for more information.",
                 "Portuguese": f"'{subs}' no es válido. \n Adicione o ID do jogador. use o comando '-i' para obter mais informações."},
            "Happy":
                {"Spanish": "¡Estás felíz!",
                 "English": "You Are happy!",
                 "Portuguese": "Você está feliz!"},
            "Add Admin Msg":
                {"Spanish": f"'{subs}' Se agregó a la lista de Admins",
                 "English": f"'{subs}' Added to Admins list",
                 "Portuguese": f"'{subs}' Adicionado à lista de administradores"},
            "Delete Admin Msg":
                {"Spanish": f"Se removió a '{subs}' de la lista de Admins",
                 "English": f"'{subs}' was removed from the Admins list",
                 "Portuguese": f"'{subs}' foi removido da lista de administradores"},
            "Players Data":
                {"Spanish": "Nombre | Jugador ID | Cliente ID",
                 "English": "Name | Player ID | Client ID",
                 "Portuguese": "Nome |  Jogador ID |  ID do Cliente"},
            "Party Info":
                {"Spanish": f"{icons[0]}{subs[0]}",
                 "English": f"{icons[0]}{subs[0]}",
                 "Portuguese": f"{icons[0]}{subs[0]}"},
            "Same Player":
                  {"Spanish": "No puedes expulsarte a tí mismo",
                   "English": "You cannot expel yourself",
                   "Portuguese": "Você não pode se expulsar"},
            "Kick Msg":
                  {"Spanish": f"Sin rodeos, {subs[0]} ha expulsado a {subs[1]}",
                   "English": f"{subs[0]} kicked {subs[1]} Goodbye!",
                   "Portuguese": f"{subs[0]} expulsou {subs[1]}"},
            "User Invalid":
                {"Spanish": f"'{subs}' No le pertenece a ningún jugador.",
                 "English": f"'{subs}' Does not belong to any player.",
                 "Portuguese": f"'{subs}' Não pertence a nenhum jogador."},
            "Chat Live":
                {"Spanish": f"{icons[0]} CHAT EN VIVO {icons[0]}",
                 "English": f"{icons[0]} CHAT LIVE {icons[0]}",
                 "Portuguese": f"{icons[0]} BATE-PAPO AO VIVO {icons[0]}"},
            "Not Exists Node":
                {"Spanish": "No estás en el juego",
                 "English": "You're not in the game",
                 "Portuguese": "Você não está no jogo"},
            "Show Spaz Messages":
                {"Spanish": "Mostrar mensajes arriba de los jugadores.",
                 "English": "Show messages above players.",
                 "Portuguese": "Mostrar mensagens acima dos jogadores."},
            "Mute Message":
                {"Spanish": f"Se silenció a {subs}",
                 "English": f"{subs} was muted",
                 "Portuguese": f"{subs} foi silenciado"},
            "Unmute Message":
                {"Spanish": f"Se quitó el muteo a {subs}",
                 "English": f"{subs} can chat again",
                 "Portuguese": f"{subs} pode conversar novamente"},
            "Not In Admins":
                {"Spanish": f"No se puede silenciar a [{subs}] porque es administrador.",
                 "English": f"[{subs}] cannot be muted because he is an administrator.",
                 "Portuguese": f"[{subs}] não pode ser silenciado porque é um administrador."},
            "Module Not Found":
                {"Spanish": "No se encontraron los módulos. usa el comando '!dw' para descargarlos.",
                 "English": "Modules not found. use the '!dw' command to download them.",
                 "Portuguese": "Módulos não encontrados.  use o comando '!dw' para baixá-los."},
            "Clima Error Message":
                {"Spanish": "Selecciona un clima,\n Usa el comando '-climas' para más información.",
                 "English": "Select a weather,\n Use the command '-climas' for more information.",
                 "Portuguese": "Selecione um clima,\n Use o comando '-climas' para mais informações."},
            "Clima Message":
                {"Spanish": f"Se cambió el clima a '{subs}'",
                 "English": f"The weather is now '{subs}'",
                 "Portuguese": f"O tempo está agora '{subs}'"},
           "None Account":
                {"Spanish": "Información del jugador no válida.",
                 "English": "Informações do jogador inválidas.",
                 "Portuguese": "Informações do jogador inválidas."}, 
           "Error ID User":
                {"Spanish": f"Se produjo un error al ingresar el ID del jugador. \n '{subs}' no es válido.",
                 "English": f"An error occurred while entering the player ID. \n '{subs}' is not valid.",
                 "Portuguese": f"Ocorreu um erro ao inserir o ID do jogador.  \n '{subs}' não é válido."},
           "Effect Invalid":
                {"Spanish": f"'{subs}' es inválido. ingresa el comando '-effects' para más información.",
                 "English": f"'{subs}' is invalid. enter the command '-effects' for more information.",
                 "Portuguese": f"'{subs}' é inválido. digite o comando '-effects' para mais informações."},
           "Use -i Command":
                {"Spanish": "Le sugerimos usar el comando '-i'",
                 "English": "We suggest you use the '-i' command",
                 "Portuguese": "Sugerimos que você use o comando '-i'"},
           "Add Effect Message":
                {"Spanish": f"Se agregó el efecto '{subs[0]}' a {subs[1]}",
                 "English": f"Added '{subs[0]}' effect to {subs[1]}",
                 "Portuguese": f"Adicionado efeito '{subs[0]}' para {subs[1]}"},
           "Exe":
                {"Spanish": "Comando Ejecutado",
                 "English": "Success",
                 "Portuguese": "Comando Executado"
            },
                 
            # ES
            "Agrega un texto":
                {"Spanish": "Añade un texto",
                 "English": "Add text",
                 "Portuguese": "Adicione texto"},
            "Cambios Guardados":
                {"Spanish": "Información guardada correctamente",
                 "English": "Information saved successfully",
                 "Portuguese": "Informações salvas com sucesso"},
            "Info Color":
                {"Spanish": "Argumento no válido, \n te sugerimos usar el comando '-colors'",
                 "English": "Invalid argument, \n we suggest you use the '-colors' command",
                 "Portuguese": "Argumento inválido, \n sugerimos que você use o comando '-colors'"},
            "ID Cliente Msj":
                {"Spanish": "Agrega el ID del cliente. \n utilice el comando '-i' para más información.",
                 "English": "Add the client ID.  \n use the '-i' command for more information.",
                 "Portuguese": "Adicione o ID do cliente. \n use o comando '-i' para mais informações."},
            "Guardando Informacion":
                {"Spanish": "Estamos guardando sus datos...",
                 "English": "Saving user data...",
                 "Portuguese": "Estamos salvando seus dados..."},
            "Ban A Admin Mensaje":
                {"Spanish": f"No puedes expulsar a [{subs}] porque es administrador",
                 "English": f"You can't kick [{subs}] because he's an admin",
                 "Portuguese": f"Você não pode chutar [{subs}] porque ele é um administrador"},
            "No Info Activa":
                {"Spanish": "Necesitas tener activa la información.\n Usa el comando '-info' para activarle.",
                 "English": "You need to have info active.\n Use the '-info' command to activate it",
                 "Portuguese": "Você precisa ter as informações ativas.\n Use o comando '-info' para ativá-las"},
                     }
    
        language = ["Spanish", "English", "Portuguese"]
        if lang not in language:
            lang = "English"
            
        if text not in setphrases:
            self.text = text
        else:
            self.text = setphrases[text][lang]
    
    def get(self):
        return self.text

def getlanguage(*args, **kwargs) -> str:
    subs = kwargs.get('subs', 'none')
    
    if type(subs) is not list:
        subs = str(subs)
    else:
        subs = [str(s) for s in subs]
    try:
        text = Lang(*args, subs=subs).get()
    except (IndexError, Exception):
        text = Lang(*args).get()
        text = text.replace('none', str(subs))
    finally:
        return text

calls: dict[str, Any] = {}
Chats: list[str] = []
roster = bs.get_game_roster
act = bs.get_foreground_host_activity
mutelist = list()

cfg = dict()

class PopupText(ptext.PopupText):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.node.shadow = 1.5
        self.node.color = (1.0, 1.0, 1.0, 1.0)
        bs.animate(self._combine, 'input3', {0: 0, 0.1: 1.0})
        
    def handlemessage(self, msg: Any) -> Any:
        pass
    
class Commands:

    fct: CommandFunctions
    "Llama los distintos comandos"
    
    util: Uts
    "Llama a las distintas utilidades"
    
    @property
    def get(self) -> str:
        return self.value
    
    def __init__(self,
                 msg: str,
                 client_id: int,
                 arguments: list[str] = []) -> None:
            
        self.message = msg
        self.msg = msg.strip()
        self.client_id = client_id
        self.arguments = arguments
        self.value = None

        self.util = Uts
        self.fct = CommandFunctions

        self.filter_chat()
        
    def clientmessage(self, msg: str,
            color: Sequence[float] = None):
                
        self.util.sm(msg, color=color,
            transient=True,
            clients=[self.client_id])

    def set_permanent_name(self, ms: list[str],
            ClientMessage: Callable) -> None:
        # /name <id|a> <new name...>
        # Sets a PERMANENT name for the account behind that client (the
        # same account tied to their android/Google Play/v2 identity), not
        # just the current life/session. It stays until changed again.
        try:
            target = ms[1]
            new_name = ' '.join(ms[2:])
            if not new_name:
                raise IndexError
        except IndexError:
            ClientMessage(getlanguage('EJ',
                subs=ms[0] + ' -1  Mamad | ' + ms[0] + ' 0  Mamad | ' + ms[0] + ' all Mamad'), color=(2, 0, 6))
            return

        if target in ('a', 'all'):
            targets = list(self.util.accounts.keys())
        elif target == '-1':
            targets = [self.client_id]
        else:
            try:
                targets = [int(target)]
            except ValueError:
                ClientMessage(getlanguage('Error Entering Player ID', subs=target), color=(1, 0, 0))
                return

        applied = False
        for c_id in targets:
            # Resolve (and, if needed, create) the account record behind
            # this client so 'name -1 <name>' always works for yourself,
            # even if this client hasn't been linked into
            # self.util.accounts yet (e.g. update_usernames() hasn't run
            # since you joined). Without this, renaming yourself could
            # silently do nothing the first time you tried it.
            if c_id not in self.util.accounts:
                account_id = self.util.userpbs.get(c_id)
                if account_id is None:
                    player = self.util.players.get(c_id)
                    try:
                        account_id = (player.get_v1_account_id()
                            if player is not None and player.exists() else None)
                    except Exception:
                        account_id = None

                if account_id is not None:
                    if account_id not in self.util.pdata:
                        self.util.add_player_data(account_id)
                    self.util.accounts[c_id] = self.util.pdata[account_id]
                    self.util.userpbs[c_id] = account_id

            if c_id not in self.util.accounts:
                ClientMessage(getlanguage('User Invalid', subs=c_id), color=(1, 0.5, 0))
                continue

            # Written straight into the account's saved record (below),
            # keyed by the account's real v1/v2 id -- not the temporary
            # client id -- so it's permanent and survives reconnects.
            self.util.accounts[c_id]['Name'] = new_name
            self.util.usernames[c_id] = new_name
            self.util.shortnames[c_id] = new_name
            self.fct.apply_permanent_name(c_id, new_name)
            applied = True

        if applied:
            self.util.save_players_data()
            ClientMessage(getlanguage('Cambios Guardados'), color=(2, 0, 6))
    
    def filter_chat(self) -> None:
        ms = self.arguments
        self.util.update_usernames()
                
        if self.client_id in self.util.accounts:
            if self.util.accounts[self.client_id]['Mute']:
                return setattr(self, 'value', '@')
        
        if cfg['Commands'].get('ShowMessages'):
            cls_node = self.fct.get_actor(self.client_id)
            if cls_node is not None:
                ActorMessage(self.msg, cls_node)
        
        if 'info' in ms[0].lower():
            with act().context:
                bs.timer(0.01, bs.Call(self.util.create_data_text, act()))
                
        with act().context:
            bs.timer(0.01, bs.Call(self.util.create_live_chat, act(),
                chat=[self.client_id, self.message],
                admin=self.fct.user_is_admin(self.client_id)))
    
        self.command_all()
        
        if self.fct.user_is_admin(self.client_id):
            self.admin_commands()
    
    def command_all(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cmd = self.fct.all_cmd()
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage
    
        if msg.lower() == cmd[0]: # -i
            self.fct.get_user_list(self.client_id)
    
        elif msg.lower() == cmd[1]: # -pb
            self.util.cm("معرفی کنید \ue043D4RKS0UL_8\ue043سرور بی اس لاین سازنده : ")
            #return setattr(self, 'value', '@')
            
        elif msg.lower() == cmd[2]: # -ceb
            self.fct.actor_command(ms=ms,
                call=self.fct.celebrate,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('خوشحالی'), color=(1.0, 1.0, 0.0))
            
        elif msg.lower() == cmd[3]: # -wave
            self.fct.actor_command(ms=ms,
                call=self.fct.wave,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('سلام!'), color=(0, 1, 3))

        elif msg.lower() == cmd[4]: # -colors
            cols = str()
            cols_list = self.util.sort_list(self.utils.colors())
            for c in cols_list:
                cols += ('♧'.join(c) + '\n')
            ClientMessage(cols)
            
        elif msg.lower() == cmd[5]: # -mp (max players)
            mp = bs.get_public_party_max_size()
            ClientMessage(bs.Lstr(value='${LSTR}: ${COUNT}',
                    subs=[('${LSTR}', bs.Lstr(resource='maxPartySizeText')),
                          ('${COUNT}', str(mp))]))

        elif msg.lower() == cmd[6]: # -pb
            self.fct.get_my_pb(self.client_id)
    
        elif msg.lower() == cmd[7]: # -effects
            cols = str()
            for e in self.fct.effects():
                cols += (' | ' + e)
            ClientMessage(cols)
        
        elif msg.lower() == cmd[8]: # -commands
            cols = str()
            for e in self.fct.admins_cmd():
                cols += ('^' + e)
            ClientMessage(cols)

        elif msg.lower() == cmd[9]: # -char
            self.fct.actor_command(ms=ms,
                call=self.fct.textor,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('تست قشنگم'), color=(2, 0, 6))

    def admin_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        ms[0] = ms[0].lower()
        cmd = [cd.lower() for cd in self.fct.admins_cmd()]
    
        if ms[0] == cmd[0]: # /name 0 Mamad
            self.set_permanent_name(ms, ClientMessage)
    
        elif ms[0] == cmd[1]: # /imp
            self.fct.actor_command(ms=ms,
                call=self.fct.impulse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('ضربه بی آسیب'), color=(2, 0, 6))
            
        elif ms[0] == cmd[2]: # /box
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_box,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('کاراکتر زو'), color=(2, 0, 6))
                               
        elif ms[0]  == cmd[3]: # /fl
            self.fct.actor_command(ms=ms,
                call=self.fct.fl,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('پرواز دو بعدی'), color=(2, 0, 6))

        elif ms[0]  == cmd[4]: # /zoe
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_box,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('تست قشنگم'), color=(2, 0, 6))
                        
        elif ms[0] == cmd[5]: # /kill
            self.fct.actor_command(ms=ms,
                call=self.fct.kill_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('کشته شد'), color=(2, 0, 6))
                        
        elif ms[0] == cmd[6]: # -pause
            self.fct.pause()
            ClientMessage(getlanguage('توقف'), color=(2, 0, 6))
                        
        elif ms[0] == cmd[7]: # /infoHost
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('info بنویس'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Agrega un texto'))
                else:
                    cfg['Commands']['HostName'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage(getlanguage('نوشته تنظیم شد'), color=(0.0, 1.0, 0.0))
                
        elif ms[0] == cmd[8]: # /night
            with act().context:
                bs.getactivity().globalsnode.tint = (0.394, 0.4421, 0.7342)
                ClientMessage(getlanguage('شب تیره...'), color=(0.3, 0.23, 0.41))

        elif ms[0] == cmd[9]: # -info
            if cfg['Commands'].get('ShowInfo'):
                cfg['Commands']['ShowInfo'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowInfo'] = True
                color = self.util.colors()['green']
                
            self.util.save_settings()
            ClientMessage(getlanguage('ذخیره شد'), color=(0, 1, 0))
    
        elif ms[0] == cmd[10]: # /infoColor
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Info Color'))
                else:
                    if ms[1] not in self.util.colors():
                        ClientMessage(getlanguage('Info Color'), color=(1, 0.5, 0))
                    else:
                        cfg['Commands']['InfoColor'] = self.int[tuple]
                        self.util.save_settings()
                        ClientMessage(getlanguage('رنگ تعیین شد'), color=(1, 1, 0))
    
        elif ms[0] == cmd[11]: # -end
            with act().context:
                act().end_game()
                ClientMessage(getlanguage('بازی تمام شد'), color=(2, 0, 6))
    
        elif ms[0] == cmd[12]: # /kick
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except Exception as exc:
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(
                            getlanguage('Error Entering Client ID',
                                subs=[ms[1], ms[0] + ' 113']))
                    else:
                        ClientMessage(f'{type(e).__name__}: {e}')
                else:
                    if self.client_id == c_id:
                        ClientMessage(getlanguage('Same Player'))
                    else:
                        if c_id not in self.util.usernames:
                            ClientMessage(getlanguage('User Invalid', subs=c_id))
                        else:
                            user1 = self.util.usernames[self.client_id]
                            user2 = self.util.usernames[c_id]
                            if self.fct.user_is_admin(c_id):
                                ClientMessage(getlanguage('Ban A Admin Mensaje', subs=user2))
                            else:
                                self.util.cm(getlanguage('Kick Msg', subs=[user1, user2]))
                                bs.disconnect_client(c_id)
                                ClientMessage(getlanguage('کیک شد'), color=(2, 0, 6))
    
        elif ms[0] == cmd[13]: # /-chatLive
            if cfg['Commands'].get('ChatLive'):
                cfg['Commands']['ChatLive'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ChatLive'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage(getlanguage('تنظیم شد'), color=(2, 0, 6))
    
        elif ms[0] == cmd[14]: # /freeze
            self.fct.actor_command(ms=ms,
                call=self.fct.freeze_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('یخ زد'), color=(2, 0, 6))
            
        elif ms[0] == cmd[15]: # /playerColor
            try: color = ms[2]
            except IndexError:
                ClientMessage(getlanguage('Info Color'))
                ClientMessage(getlanguage('EJ',
                    subs=ms[0] + ' 0  yellow | ' + ms[0] + ' all green'))
            else:
                self.fct.actor_command(ms=ms,
                    call=bs.Call(self.fct.player_color, color),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
                ClientMessage(getlanguage('رنگ بازیکن تعیین شد'), color=(2, 0, 6))
    
        elif ms[0] == cmd[16]: # /maxPlayers
            try:
                val = int(ms[1])
            except:
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 5'))
            else:
                bs.set_public_party_max_size(val)
                ClientMessage(
                    bs.Lstr(value='${LSTR}: ${COUNT}',
                        subs=[('${LSTR}', bs.Lstr(resource='maxPartySizeText')),
                              ('${COUNT}', ms[1])]))
    
        elif ms[0] == cmd[17]: # -showMessages
            if cfg['Commands'].get('ShowMessages'):
                cfg['Commands']['ShowMessages'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowMessages'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage(getlanguage('ذخیره شد'), color=(2, 0, 6))
    
        elif ms[0] == cmd[18]: # /sleep
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sleep,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('خواب'), color=(2, 0, 6))
    
        elif ms[0] == cmd[19] or ms[0] == cmd[20]: # /mute /unmute
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except Exception as e:
                    ClientMessage(
                        getlanguage('Error Entering Client ID',
                            subs=[ms[1], ms[0] + ' 113']))
                else:
                    if c_id not in self.util.accounts:
                        ClientMessage(getlanguage('User Invalid', subs=c_id))
                    else:
                        user = self.util.usernames[c_id]
                        if ms[0] == cmd[19]:
                            if self.fct.user_is_admin(c_id):
                                self.util.cm(getlanguage('Not In Admins', subs=Uts.usernames[c_id]))
                                return
                            if not self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = True
                                self.util.cm(getlanguage('Mute Message', subs=user))
                        elif ms[0] == cmd[20]:
                            if self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = False
                                self.util.cm(getlanguage('Unmute Message', subs=user))
                        Uts.save_players_data()

        elif ms[0] == cmd[21]: # /gm
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gm,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('ضد ضربه'), color=(2, 0, 6))
    
        elif ms[0] == cmd[22]: # -slow
            self.fct.slow()
            ClientMessage(getlanguage('سرعت بازی'), color=(2, 0, 6))

        elif ms[0] == cmd[23]: # /speed
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_speed,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('سرعت'), color=(2, 0, 6))
                      
        elif ms[0] == cmd[24]: # /effect
            try:
                c_id = int(ms[1])
                eff = ms[2]
            except ValueError:
                ClientMessage(getlanguage('Error ID User', subs=ms[1]), color=(1, 0, 0))
            except IndexError:
                ClientMessage(getlanguage('ID Cliente Msj'), color=(1, 0.5, 0))
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 113 fire'), color=(1, 0.5, 0))
            else:
                if c_id not in self.util.accounts:
                    ClientMessage(getlanguage('User Invalid', subs=c_id), color=(1, 0.5, 0))
                    ClientMessage(getlanguage('Use -i Command'), color=(1, 0.5, 0))
                else:
                    if eff not in self.fct.effects():
                        ClientMessage(getlanguage('Effect Invalid', subs=eff), color=(1, 0.5, 0))
                    else:
                        self.util.accounts[c_id]['Effect'] = eff
                        self.util.save_players_data()
                        self.util.cm("d")
                        user = self.util.usernames[c_id]
                        ClientMessage(getlanguage('Add Effect Message',
                            subs=[eff, user]), color=(0, 0.5, 1))

        elif ms[0] == cmd[25]: # /punch
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_punch,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('مشت قدرتی'), color=(2, 0, 6))
        
        elif ms[0] == cmd[26]: # /gloves
            self.fct.actor_command(ms=ms,
                call=self.fct.gloves,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('قدرت زیاد'), color=(2, 0, 6))
                       
        elif ms[0] == cmd[27]: # /mbox
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_mgb,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('جعبه جاذبه'), color=(2, 0, 6))
                       
        elif ms[0] == cmd[28]: # /drop
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_drop,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('بمب خواب'), color=(2, 0, 6))

        elif ms[0] == cmd[29]: # /gift
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gift,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('هدیه نفیس'), color=(2, 0, 6))
                       
        elif ms[0] == cmd[30]: # /curse
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_curse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('بمب ساعتی'), color=(2, 0, 6))
                       
        elif ms[0] == cmd[31]: # /unfreeze
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_unfreeze,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('یخ شکن'), color=(2, 0, 6))

        elif ms[0] == cmd[32]: # /superjump
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sjump,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('پرواز'), color=(2, 0, 6))
           
        elif ms[0] == cmd[33]: # /health
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_health,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('خون'), color=(2, 0, 6))

        elif ms[0] == cmd[34]: # /shield
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_shield,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('سپر'), color=(2, 0, 6))

        elif ms[0] == cmd[35]: # /power
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_power,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('بوکسور'), color=(2, 0, 6))

        elif ms[0] == cmd[36]: # /fastpunch
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_fastpunch,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('مشت سریع'), color=(2, 0, 6))

        elif ms[0] == cmd[37]: # /fifbombs
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_fifbombs,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('بمب پنجتایی'), color=(2, 0, 6))

        elif ms[0] == cmd[38]: # /superbombs
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_superbombs,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('بمب قوی'), color=(2, 0, 6))
                      
        elif ms[0] == cmd[39]: # /hug a | /hug 2 | /hug 2 3
            if len(ms) < 2:
                ClientMessage(getlanguage('EJ',
                    subs=ms[0] + ' a | ' + ms[0] + ' 2 | ' + ms[0] + ' 2 3'))
            elif ms[1] == 'a':
                self.fct.hug_all()
                ClientMessage(getlanguage('بغل'), color=(2, 0, 6))
            else:
                try:
                    if len(ms) >= 3:
                        holder_id = int(ms[1])
                        target_id = int(ms[2])
                    else:
                        holder_id = self.client_id
                        target_id = int(ms[1])
                except ValueError:
                    ClientMessage(getlanguage('Error Entering Player ID', subs=ms[1]), color=(1, 0, 0))
                else:
                    if self.fct.hug(holder_id, target_id):
                        ClientMessage(getlanguage('بغل'), color=(2, 0, 6))
                    else:
                        ClientMessage(getlanguage('User Invalid', subs=target_id), color=(1, 0.5, 0))

        elif ms[0] == cmd[40]: # /t 1 0 0
            try:
                r = float(ms[1])
                g = float(ms[2])
                b = float(ms[3])
            except (IndexError, ValueError):
                ClientMessage(getlanguage('Info Color'))
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 1 0 0'))
            else:
                self.fct.tint(r, g, b)
                ClientMessage(getlanguage('رنگ مپ تعیین شد'), color=(2, 0, 6))

        elif ms[0]  == cmd[41]: # /text
            self.fct.actor_command(ms=ms,
                call=self.fct.text,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('تست'), color=(2, 0, 6))

        elif ms[0]  == cmd[42]: # /light
            bs.getactivity().globalsnode.reflection =  Character
            ClientMessage(getlanguage('تسست'), color=(2, 0, 6))

        elif ms[0]  == cmd[43]: # /suffer
            self.fct.actor_command(ms=ms,
                call=self.fct.suffer,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('عذاب تی ان تی'), color=(0.8, 1.5, 1.5))

        elif ms[0] == cmd[44]: # /effect
            try:
                c_id = int(ms[1])
                eff = ms[2]
            except ValueError:
                ClientMessage(getlanguage('Error ID User', subs=ms[1]), color=(1, 0, 0))
            except IndexError:
                ClientMessage(getlanguage('ID Cliente Msj'), color=(1, 0.5, 0))
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 113 fire'), color=(1, 0.5, 0))
            else:
                if c_id not in self.util.accounts:
                    ClientMessage(getlanguage('User Invalid', subs=c_id), color=(1, 0.5, 0))
                    ClientMessage(getlanguage('Use -i Command'), color=(1, 0.5, 0))
                else:
                    if eff not in self.fct.effects():
                        ClientMessage(getlanguage('Effect Invalid', subs=eff), color=(1, 0.5, 0))
                    else:
                        self.util.accounts[c_id]['Effect'] = eff
                        self.util.save_players_data()
                        self.util.cm("d")
                        user = self.util.usernames[c_id]
                        ClientMessage(getlanguage('Add Effect Message',
                            subs=[eff, user]), color=(0, 0.5, 1))

        if ms[0] == cmd[45]: # /namee 0 Ali (alias of /name)
            self.set_permanent_name(ms, ClientMessage)

        elif ms[0] == cmd[46]: # /fly  or /fly 0  or /fly a
            self.fct.actor_command(ms=ms,
                call=self.fct.toggle_fly,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            ClientMessage(getlanguage('Exe'), color=(0, 1, 0))

class CommandFunctions:
    def all_cmd() -> list[str]:
        return [
            'i', 'by', 'cel', 'wave', 'cols',
            'mp', 'pb', 'efs', 'cmds', '~'
            ]
            
    def admins_cmd() -> list[str]:
        return [
            'name', 'imp', 'zoe', 'fl',
            'char', 'd', 'pause', 'ides',
            'n', 'info', 'tcol', 'e',
            'kick', 'live', 'fr', 'col',
            'max', 'msg', 'sl',
            'mute', 'unmute', 'g', 'sm', 'sp',
            'ef', 'p', 'glo', 'mbox', 'drop', 'gift',
            'cu', 'u', 'j', 'h', 'sh', 'pun', 'fp', 'fb',
            'sb', 'hug', 't', 'dmg', 'li', 'suf', 'eff', 'namee', 'fly',
            ]

    def effects() -> list[str]:
        return ['none', 'footprint', 'fire', 'darkmagic',
                'particle', 'stars', 'smoke', 'loops', 'spark', 'hole', 'rainbow']

    def get_my_pb(client_id: int) -> None:
        print(Uts.userpbs)
        if Uts.userpbs.get(client_id):
            pb = Uts.userpbs[client_id]
            Uts.sm(pb, transient=True, clients=[client_id])

    def fl(node: bs.Node) -> None:
        with act().context:
            if node.fly:
                node.fly = False
            else:
                node.fly = True

    # /fly -- a custom flight mode, separate from the built-in /fl noclip
    # toggle above. While active:
    #  - a glowing circular aura in the player's body color (node.color,
    #    NOT node.highlight) follows their torso in real time and grows
    #    with height off the ground, shrinks back down near it.
    #  - pressing jump gives a boost impulse (stronger than a normal
    #    jump) aimed mostly upward, nudged slightly by whatever direction
    #    the joystick is currently held, so repeated jumps let the player
    #    steer instead of just launching straight up every time. node
    #    velocity isn't writable on a spaz node, so this has to go
    #    through a real 'impulse' message -- but at a magnitude strong
    #    enough to lift the character, the engine treats it like a hit
    #    and can trigger the ragdoll/knockout reaction. fly_jump_boost()
    #    below fires the impulse and then immediately clears any
    #    knockout it caused on the next few ticks, so it still reads as
    #    a harmless lift rather than getting knocked out. Called from
    #    the jump-press hook.
    FLY_AURA_BASE_RADIUS = 0.6
    FLY_AURA_HEIGHT_SCALE = 0.35
    FLY_BOOST_UP = 6.5
    FLY_BOOST_MAGNITUDE = 550.0
    FLY_STEER_SCALE = 1.4           # how much the joystick nudges the boost sideways
    # NOTE: there's no confirmed "torso only" hit attribute in the public
    # node API, so this targets the impulse at the character's own
    # position with a small radius as the closest achievable match --
    # tune FLY_IMPULSE_RADIUS if it's catching more than the torso.
    FLY_IMPULSE_RADIUS = 2.5
    # How many ticks after the boost impulse to clear a ragdoll/knockout
    # reaction it may have triggered. The engine can apply the reaction
    # a tick or two after the impulse lands, so we clear on several
    # consecutive ticks rather than just once.
    FLY_KNOCKOUT_CLEAR_TICKS = (0, 1, 2, 3)

    def toggle_fly(node: bs.Node) -> None:
        actor = getattr(node, 'source_player', None)
        actor = actor.actor if actor is not None else None
        if actor is None:
            return

        with act().context:
            if getattr(actor, '_cm_fly', False):
                actor._cm_fly = False
                actor._cm_fly_aura_timer = None
                aura = getattr(actor, '_cm_fly_aura_node', None)
                if aura is not None and aura.exists():
                    aura.delete()
                actor._cm_fly_aura_node = None
                actor._cm_fly_base_y = None
            else:
                actor._cm_fly = True
                actor._cm_fly_base_y = node.position[1]
                actor._cm_fly_aura_node = bs.newnode('light', attrs={
                    'position': node.position,
                    'radius': CommandFunctions.FLY_AURA_BASE_RADIUS,
                    'color': node.color,
                    'lights_volumes': False,
                })
                actor._cm_fly_aura_timer = bs.Timer(0.03,
                    bs.Call(CommandFunctions._update_fly_aura, actor), repeat=True)

    def _update_fly_aura(actor) -> None:
        node = getattr(actor, 'node', None)
        aura = getattr(actor, '_cm_fly_aura_node', None)

        if (not getattr(actor, '_cm_fly', False)
                or node is None or not node.exists()
                or aura is None or not aura.exists()):
            actor._cm_fly_aura_timer = None
            return

        with act().context:
            pos = node.position
            base_y = getattr(actor, '_cm_fly_base_y', pos[1])
            height = max(0.0, pos[1] - base_y)

            aura.position = pos
            aura.radius = (CommandFunctions.FLY_AURA_BASE_RADIUS
                + height * CommandFunctions.FLY_AURA_HEIGHT_SCALE)
            aura.color = node.color  # keep matching body color if it changes

    def fly_jump_boost(actor) -> None:
        node = getattr(actor, 'node', None)
        if node is None or not node.exists():
            return

        # Current joystick tilt, used to steer the boost a little.
        lr = getattr(node, 'move_left_right', 0.0) or 0.0
        ud = getattr(node, 'move_up_down', 0.0) or 0.0

        vx = lr * CommandFunctions.FLY_STEER_SCALE
        vz = -ud * CommandFunctions.FLY_STEER_SCALE
        vy = CommandFunctions.FLY_BOOST_UP

        with act().context:
            pos = node.position
            node.handlemessage('impulse',
                pos[0], pos[1], pos[2],
                vx, vy, vz,
                CommandFunctions.FLY_BOOST_MAGNITUDE, 0.0,
                CommandFunctions.FLY_IMPULSE_RADIUS, 0,
                0.0, 1.0, 0.0)

            # The impulse above is what actually lifts the character,
            # but at this magnitude the engine can read it as a hit and
            # start the ragdoll/knockout reaction. Clear it right after
            # (over a few ticks, since the engine may apply it a tick or
            # two after the impulse lands) so it never actually knocks
            # the character out -- just lifts them.
            for delay in CommandFunctions.FLY_KNOCKOUT_CLEAR_TICKS:
                bs.timer(delay, bs.Call(CommandFunctions._cancel_fly_knockout, actor))

    def _cancel_fly_knockout(actor) -> None:
        node = getattr(actor, 'node', None)
        if node is None or not node.exists():
            return

        with act().context:
            node.handlemessage('knockout', 0.0)

    def light(node: bs.Node) -> None:
        with act().context:
            bs.getactivity().globalsnode.reflection = Character
            bs.getactivity().globalsnode.reflection_scale = float(1.0)

    def Night(node: bs.Node) -> None:
        with act().context:
            bs.getactivity().globalsnode.tint =  (0.254, 0.2421, 0.4342)

    def tint(r: float, g: float, b: float) -> None:
        with act().context:
            bs.getactivity().globalsnode.tint = (r, g, b)

    def hug(holder_id: int, target_id: int) -> bool:
        holder_actor = CommandFunctions.get_actor(holder_id)
        # If holder and target are the same id, they hold their own head.
        target_actor = holder_actor if holder_id == target_id else CommandFunctions.get_actor(target_id)

        if holder_actor is None or getattr(holder_actor, 'node', None) is None or not holder_actor.node.exists():
            return False
        if target_actor is None or getattr(target_actor, 'node', None) is None or not target_actor.node.exists():
            return False

        with act().context:
            holder_actor.node.hold_node = target_actor.node

        return True

    def hug_all() -> None:
        actors = []
        for p in act().players:
            actor = getattr(p, 'actor', None)
            if actor is not None and getattr(actor, 'node', None) is not None and actor.node.exists():
                actors.append(actor)

        count = len(actors)
        if count == 0:
            return

        # Chain everyone in a circle so every player both holds someone
        # and is held by someone else. A single player just holds
        # themself (their own head), since there's no one else to hug.
        with act().context:
            for i, holder in enumerate(actors):
                target = actors[(i + 1) % count]
                holder.node.hold_node = target.node

    def spaz_sjump(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with act().context:
            if getattr(actor, 'cm_superjump', None):
                actor.cm_superjump = False
            else:
                actor.cm_superjump = True
                
    def spaz_unfreeze(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(bs.ThawMessage())

    def spaz_curse(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(bs.PowerupMessage('curse', node))
  
    def spaz_health(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(bs.PowerupMessage('health', node))
    
    def spaz_shield(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(bs.PowerupMessage('shield', node))
          
    def spaz_power(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
         
        with act().context:
            actor._punch_power_scale = 2.5
            actor._holdNode = actor

    def celebrate(node: bs.Node) -> Node:
        with act().context:
            node.handlemessage(bs.CelebrateMessage(10.0))
            bs.getsound('crowdChant').play(5)
            bs.getsound('cheer').play(5)

    def wave(node: bs.Node) -> Node:
        with act().context:
            waves = ['celebrate_r', 'celebrate_l']
            node.handlemessage(random.choice(waves), (4000.0))

    def spaz_fastpunch(node: bs.node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.

        with act().context:
            actor._punch_cooldown = 150

    def spaz_fifbombs(node: bs.node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
         
        with act().context:
                actor.bomb_count = 5

    def spaz_superbombs(node: bs.node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
         
        with act().context:
                actor.blast_radius = 5

    def spaz_gift(node: bs.Node) -> None:
        with act().context:
            ExplosiveGift(owner=node)
    
    def spaz_mgb(node: bs.Node) -> None:
        with act().context:
            MagicBox(pos=node.position).autoretain()
            
    def suffer(node: bs.Node) -> None:
        with act().context:
            suffertnt(pos=node.position).autoretain()
            

    def spaz_punch(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with act().context:
            actor._punch_power_scale = 10.0
            
    def spaz_speed(node: bs.Node) -> None:
        with act().context:
            if node.hockey:
                node.hockey = False
            else:
                node.hockey = True

    def slow() -> None:
        with act().context:
            gnode = act().globalsnode
            if gnode.slow_motion:
                gnode.slow_motion = False
            else:
                gnode.slow_motion = True
            
    def spaz_gm(node: bs.Node) -> None:
        with act().context:
            if node.invincible:
                node.invincible = False
            else:
                node.invincible = True
            
    def spaz_sleep(node: bs.Node) -> None:
        with act().context:
            for x in range(1):
                bs.timer(x, bs.Call(node.handlemessage, 'knockout', 3000.0))
            
    def spaz_name(name: str, node: bs.Node) -> None:
        with act().context:
            node.name = name

    # Dynamic overhead name: light-blue text with a dark-blue offset shadow.
    # The built-in nametag is disabled so it does not create a third copy.
    NAME_COLOR = (0.55, 0.85, 1.0)

    # Tune these to change the look.
    NAME_TEXT_COLOR = (0.75, 0.95, 2.9)       # bright/light blue
    NAME_SHADOW_COLOR = (0.02, 0.05, 0.45)    # dark blue
    NAME_TEXT_SCALE = 0.0155
    NAME_SHADOW_SCALE = 0.0165                # slightly larger = clean outline
    NAME_HEIGHT_OFFSET = (0.0, 1.42, 0.0)
    NAME_SHADOW_OFFSET = (0.0, -0.015, 0.0)  # small lower/right overlap

    @staticmethod
    def _delete_nametag(actor) -> None:
        actor._cm_nametag_timer = None

        for attr in ('_cm_name_shadow_node', '_cm_name_text_node'):
            old_node = getattr(actor, attr, None)
            if old_node is not None:
                try:
                    if old_node.exists():
                        old_node.delete()
                except Exception:
                    pass
            setattr(actor, attr, None)

    def apply_permanent_name(c_id: int, name: str) -> None:
        actor = CommandFunctions.get_actor(c_id)
        if actor is None:
            return
        node = getattr(actor, 'node', None)
        if node is None or not node.exists():
            return
        with act().context:
            shadow = getattr(actor, '_cm_name_shadow_node', None)
            text_node = getattr(actor, '_cm_name_text_node', None)
            if (shadow is None or not shadow.exists()
                    or text_node is None or not text_node.exists()):
                CommandFunctions._delete_nametag(actor)
                node.name = ""
                node.name_color = CommandFunctions.NAME_COLOR
                
                h = CommandFunctions.NAME_HEIGHT_OFFSET
                s = CommandFunctions.NAME_SHADOW_OFFSET
                
                actor._cm_name_shadow_node = bs.newnode('text', owner=node, attrs={
                    'text': name, 'in_world': True,
                    'color': CommandFunctions.NAME_SHADOW_COLOR,
                    'scale': CommandFunctions.NAME_SHADOW_SCALE,
                    'h_align': 'center', 'v_align': 'center'})
                    
                actor._cm_name_text_node = bs.newnode('text', owner=node, attrs={
                    'text': name, 'in_world': True,
                    'color': CommandFunctions.NAME_TEXT_COLOR,
                    'scale': CommandFunctions.NAME_TEXT_SCALE,
                    'h_align': 'center', 'v_align': 'center'})

                math_text = bs.newnode('math', owner=node, attrs={
                    'input2': h, 'operation': 'add'})
                node.connectattr('position', math_text, 'input1')
                math_text.connectattr('output', actor._cm_name_text_node, 'position')

                math_shadow = bs.newnode('math', owner=node, attrs={
                    'input2': (h[0]+s[0], h[1]+s[1], h[2]+s[2]), 'operation': 'add'})
                node.connectattr('position', math_shadow, 'input1')
                math_shadow.connectattr('output', actor._cm_name_shadow_node, 'position')
            else:
                text_node.text = name
                shadow.text = name
                node.name = ""


    def _update_nametag_position(actor) -> None:
        node = getattr(actor, 'node', None)

    def player_color(color: str, node: bs.Node) -> None:
        with act().context:
            node.color = Uts.colors()[color]
            
    def freeze_spaz(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with act().context:
            if actor.shield:
                actor.shield.delete()
                
            actor.handlemessage(bs.FreezeMessage())

        with act().context:
            if actor.shield:
                actor.shield.delete()
                
            actor.handlemessage(bs.FreezeMessage(freeze))

    def pause() -> None:
        with act().context:
            globs = act().globalsnode
            if globs.paused:
                globs.paused = False
            else:
                globs.paused = True

    def kill_spaz(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(
                bs.DieMessage())

    def spaz_box(node: bs.Node) -> None:
        with act().context:
            node.color_texture = bs.gettexture('zoeColor')
            node.color_mask_texture = bs.gettexture('zoeColorMask')
            node.head_mesh = bs.getmesh('zoeHead')
            node.torso_mesh = bs.getmesh('zoeTorso')
            node.pelvis_mesh = bs.getmesh('zoePelvis')
            node.upper_arm_mesh = bs.getmesh('zoeUpperArm')
            node.forearm_mesh = bs.getmesh('zoeForeArm')
            node.hand_mesh = bs.getmesh('zoeHand')
            node.upper_leg_mesh = bs.getmesh('zoeUpperLeg')
            node.lower_leg_mesh = bs.getmesh('zoeLowerLeg')
            node.toes_mesh = bs.getmesh('zoeToes')
            node.style = 'female' 

    def impulse(node: bs.Node) -> None:

        msg = bs.HitMessage(pos=node.position,
                            velocity=node.velocity,
                            magnitude=300,
                            hit_subtype='imp',
                            radius=20)
                          
        if isinstance(msg, bs.HitMessage):
            for i in range(2):
                with act().context:
                    node.handlemessage(
                        'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                        msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                        msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                        msg.force_direction[1], msg.force_direction[2])

    def actor_name(name: str, node: bs.Node) -> None:
        with act().context:
            node.name = name

    def actor_command(
            ms: list[str],
            call: Callable,
            attrs: dict[str, Any]) -> None:
        ClientMessage = attrs['ClientMessage']
                
        def new_call(node: bs.Node):
            ClientMessage(getlanguage('Exe'), color=(0, 1, 0))
            call(node)
                
        if len(ms) == 1:
            if attrs['Actor'] is None:
                ClientMessage(getlanguage('Not Exists Node'))
            else:
                actor = attrs['Actor']
                new_call(actor.node)
        else:
            if ms[1] == 'a':
                for p in act().players:
                    node = p.actor.node
                    new_call(node)
            else:
                try:
                    p_id = int(ms[1])
                    node = act().players[p_id].actor.node
                except Exception as exc:
                    color = Uts.colors()['orange']
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(getlanguage('Error Entering Player ID', subs=ms[1]), color=color)
                    elif type_error is IndexError:
                        ClientMessage(getlanguage('User Invalid', subs=p_id), color=color)
                    else:
                        ClientMessage(f'{type(e).__name__}: {e}')
                    ClientMessage(getlanguage('EX', subs=ms[0] + ' 0 | ' + ms[0] + ' a'))
                else:
                    new_call(node)

    def spaz_drop(node: bs.Node) -> None:
        self = node.source_player.actor
        del node # Unused by default.

        def drop():
            pos = self.node.position
            psts = [
                (pos[0]-1,pos[1]+4,pos[2]+1),
                (pos[0]+1,pos[1]+4,pos[2]+1),
                (pos[0],pos[1]+4,pos[2]-1),
                (pos[0]-2,pos[1]+4,pos[2]),
                (pos[0]+2,pos[1]+4,pos[2]),
                (pos[0]+2,pos[1]+4,pos[2]-1),
                (pos[0]-2,pos[1]+4,pos[2]-1),
                (pos[0],pos[1]+4,pos[2]+2)]
                
            for p in psts:
                bomb = Bomb(
                    position=p,
                    bomb_scale=1.3,
                    bomb_type='sticky').autoretain()
                bomb.node.gravity_scale = 4.0
                bomb.node.color_texture = bs.gettexture('bombStickyColor')
                    
        for x in range(2):
            with act().context:
                bs.timer(x * 0.308, drop)

    def get_user_list(c_id: int) -> None:
        def delete_text(t_id: int):
            if t_id == id(act()._ids.node):
                act()._ids.node.opacity = 0.0
            
        def gText(txt: str):
            act()._ids = text.Text(txt, position=(-0.0, 270.0),
                h_align=text.Text.HAlign.CENTER, scale=1.1,
                transition=text.Text.Transition.FADE_IN).autoretain()
            act()._ids.node.opacity = 0.5
            
            t_id = id(act()._ids.node)
            bs.timer(8.0, bs.Call(delete_text, t_id))
    
        txt = str()
        txts = [getlanguage('Players Data'),
                "______________________"]

        try:
            players = act().players
        except Exception:
            players = []
        else:
            for idx, p in enumerate(players):
                if p.is_alive():
                    s = p.sessionplayer
                    c_id = s.inputdevice.client_id
                    dn = Uts.get_display_name(c_id, fallback=s.getname(False))
                    txts.append(f"{dn} | {idx} | {c_id}")
        
        txt = '\n'.join(txts)

        with act().context:
            try:
                if act()._ids.node.exists():
                    act()._ids.node.delete()
                    gText(txt)
            except AttributeError:
                gText(txt)
        bs.screenmessage(txt, clients=[c_id], transient=True)
    
    def get_characters() -> list[str]:
        return bs.app.spaz_appearances
    
    def user_is_admin(c_id: int) -> bool:
        if c_id == -1:
            return True
    
        if c_id in Uts.accounts:
            return Uts.accounts[c_id]['Admin']
        else:
            return False
    
    def get_actor(c_id: int) -> spaz.Spaz:
        act = bs.get_foreground_host_activity()
        for player in act.players:
            if c_id == player.sessionplayer.inputdevice.client_id:
                return player.actor
        
def ActorMessage(msg: str, actor: spaz.Spaz):
    def die(node: bs.Node):
        if node.exists():
            bs.animate(popup.node, 'opacity', {0: 1.0, 0.1: 0.0})
            bs.timer(0.1, popup.node.delete)
        
    with act().context:
        if getattr(actor, 'my_message', None):
            actor.my_message.node.delete()
        
        c = (1.0, 1.0, 1.0)
        position = (-0.0, 1.0, 0.0)

        m = bs.newnode('math', owner=actor.node, attrs={'input1':
            (position[0], position[1], position[2]), 'operation': 'add'})
        actor.node.connectattr('position_center', m, 'input2')

        actor.my_message = popup = PopupText(
             text=msg, color=c, scale=1.2).autoretain()
        m.connectattr('output', popup.node, 'position')
        bs.timer(4.0, bs.Call(die, popup.node))









# Effects
def _fire(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(
            position=self.node.position,
            velocity=(0, 12, 0),
            count=3,
            scale=1.5,
            spread=0.16,
            chunk_type='sweat')

        self._light = bs.newnode(
            'light',
            attrs={
                'position': self.node.position,
                'radius': 0.2,
                'color': (1.0, 0.5, 0.1),
                'lights_volumes': False,
            },
        )
        scl = float(4) / 3.75
        min_val = 0.4
        max_val = 0.7
        bs.animate(
            self._light,
            'intensity',
            {
                0.0: 0.0,
                0.250 * scl: max_val,
                0.500 * scl: min_val,
                0.750 * scl: 2.0,
                1.000 * scl: 0.0,
            },
        )
        bs.timer(0.05, self._light.delete)


        self._light = bs.newnode(
            'light',
            attrs={
                'position': self.node.position,
                'radius': 0.2,
                'color': (1.9, 0.5, 0.1),
                'lights_volumes': False,
            },
        )
        scl = float(4) / 3.75
        min_val = 0.4
        max_val = 0.7
        bs.animate(
            self._light,
            'intensity',
            {
                0.0: 0.0,
                0.25 * scl: max_val,
                0.500 * scl: min_val,
                0.750 * scl: 2.0,
                1.000 * scl: 0.0,
            },
        )
        bs.timer(0.05, self._light.delete)

def _particle(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
        scale=0.3,count=2,spread=0.1,velocity=(0, 3, 0),
        chunk_type='ice',
        emit_type='stickers'
        ),
    
        bs.emitfx(position=self.node.position,
        count=2,spread=0.3,velocity=(0, 0, 0),
        emit_type='tendrils',
        tendril_type='thin_smoke'
        ),

        bs.emitfx(position=self.node.position,
        count=2,spread=0.3,velocity=(0, 0, 0),
        emit_type='tendrils',
        tendril_type='thin_smoke'
        ),

        bs.emitfx(position=self.node.position,
        scale=0.3,count=2*2,spread=0.2,velocity=(0, 3, 0),
        chunk_type='metal'
        ),
    
        bs.emitfx(position=self.node.position,
        scale=0.3,count=2*2,spread=0.2,velocity=(0, 3, 0),
        chunk_type='ice'
        ),
    
        bs.emitfx(position=self.node.position,
        scale=0.45,count=2*2,spread=0.2,velocity=(0, 3, 0),
        chunk_type='splinter'
        ),
    
        bs.emitfx(position=self.node.position,
        scale=0.8,count=4*4,spread=0.2,velocity=(0, 3, 0),
        chunk_type='spark'
        )

def _smoke(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
        count=3,velocity=(0, 3, 0),
        emit_type='tendrils',
        tendril_type='smoke'
        ),

        bs.emitfx(position=self.node.position,
        count=3,velocity=(0, 3, 0),
        emit_type='tendrils',
        tendril_type='thin_smoke'
        )

def _hole(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        scorcher = bs.newnode(
            "scorch",
            attrs={
                "position": self.node.position,
                "size": 0.50,
                "big": True}
            )
        self.node.connectattr("position", scorcher, "position")
        animation = {
            0: (0.23,0.23,0.29),
            1: (0,0.5,0.7),
        }
        bs.animate_array(scorcher, "color", 3, animation, loop=True)
        return scorcher

        self._light = bs.newnode(
            'light',
            attrs={
                'position': self.node.position,
                'radius': 0.4,
                'color': (3.0, 0.8, 0.1),
                'lights_volumes': False,
            },
        )
        scl = float(4) / 4.75
        min_val = 0.4
        max_val = 0.7
        bs.animate(
            self._light,
            'intensity',
            {
                0.0: 0.0,
                0.25 * scl: max_val,
                0.500 * scl: min_val,
                0.750 * scl: 2.0,
                1.000 * scl: 0.0,
            },
        )
        bs.timer(0.05, self._light.delete)


        self._light = bs.newnode(
            'light',
            attrs={
                'position': self.node.position,
                'radius': 0.2,
                'color': (2.3433, 0.2567, 0.06557),
                'lights_volumes': False,
            },
        )
        scl = float(4) / 3.75
        min_val = 0.5
        max_val = 0.9
        bs.animate(
            self._light,
            'intensity',
            {
                0.0: 0.0,
                0.25 * scl: max_val,
                0.500 * scl: min_val,
                0.750 * scl: 2.0,
                1.000 * scl: 0.0,
            },
        )
        bs.timer(0.05, self._light.delete)

def footprint(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:

        loc = bs.newnode('locator', owner=self.node,
              attrs={
                     'position': self.node.position,
                     'shape': 'circle',
                     'color': self.node.color,
                     'size': [0.2],
                     'draw_beauty': False,
                     'additive': False})
        bs.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
        bs.timer(2.0, loc.delete)
    
def loops(self) -> None:
    def anim(node: bs.Node) -> None:
        bs.animate_array(node, 'color', 3,
            {0: (1,1,1), 0.1: (0,0,1),
             0.2: (0,1,1), 0.3: (0,0,0),
             0.4: (0,0,1), 0.5: (0,1,1),
             0.6: (1,1,1)}, loop=True)
        bs.animate_array(node, 'size', 1,
            {0: [1.0], 0.2: [1.5], 0.3: [1.0]}, loop=True)

    attrs = ['torso_position', 'position_center', 'position']
    for i, pos in enumerate(attrs):
        loc = bs.newnode('locator', owner=self.node,
              attrs={'shape': 'circleOutline',
                     'color': self.node.color,
                     'opacity': 1.0,
                     'draw_beauty': True,
                     'additive': False})
        self.node.connectattr(pos, loc, 'position')
        bs.timer(0.1 * i, bs.Call(anim, loc))
    
def stars(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.timer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
    
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

            texs = ['bombStickyColor', 'aliColor', 'aliColorMask', 'eggTex3']
            tex = bs.gettexture(random.choice(texs))
            mesh = bs.getmesh('flash')
            factory = SpazFactory.get()
            
            mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = bs.newnode('prop',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'mesh': mesh,
                       'mesh_scale': 0.1,
                       'body_scale': 0.0,
                       'shadow_size': 0.0,
                       'gravity_scale': 0.5,
                       'color_texture': tex,
                       'reflection': 'soft',
                       'reflection_scale': [1.5],
                       'materials': [mat]})
            
            light = bs.newnode('light',
                owner=node,
                attrs={
                    'intensity': 0.3,
                    'volume_intensity_scale': 0.5,
                    'color': (random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5)),
                    'radius': 0.035})
            node.connectattr('position', light, 'position')
            bs.timer(0.25, bs.Call(die, node))
            
def spark(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.timer(0.01, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
    
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 0.1
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.05, np[2]+p[2])
            vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

            tex = bs.gettexture('null')
            mesh = None
            factory = SpazFactory.get()
            
            mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = bs.newnode('bomb',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'mesh': mesh,
                       'mesh_scale': 0.00001,
                       'body_scale': 0.001,
                       'color_texture': tex,
                       'fuse_length': 0.000001,
                       'materials': [mat]})
            
            light = bs.newnode('light',
                owner=node,
                attrs={
                    'intensity': 0.3,
                    'volume_intensity_scale': 0.5,
                    'color': (random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5)),
                    'radius': 0.1})
            node.connectattr('position', light, 'position')
            bs.timer(0.01, bs.Call(die, node))
            
def darkmagic(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.timer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
    
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), 30.0, random.uniform(-m, m))

            tex = bs.gettexture('impactBombColor')
            mesh = bs.getmesh('impactBomb')
            factory = SpazFactory.get()
            
            mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = bs.newnode('prop',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'mesh': mesh,
                       'mesh_scale': 0.4,
                       'body_scale': 0.0,
                       'shadow_size': 0.0,
                       'gravity_scale': 0.5,
                       'color_texture': tex,
                       'reflection': 'soft',
                       'reflection_scale': [0.0],
                       'materials': [mat]})
            
            light = bs.newnode('light',
                owner=node,
                attrs={'intensity': 1.0,
                       'volume_intensity_scale': 0.5,
                       'color': (0.5, 0.0, 1.0),
                       'radius': 0.035})
            node.connectattr('position', light, 'position')
            bs.timer(0.25, bs.Call(die, node))
            
def _rainbow(self) -> None:
    animate = {
         0.0: (1.0, 0.0, 0.0),
         0.2: (2.0, 0.6, 0.0),
         0.4: (0.0, 1.25, 0.0),
         0.6: (0.0, 1.25, 1.0),
         0.8: (0.0, 0.8, 2.0),
         1.0: (0.0, 1.0, 2.0),
         1.2: (0.5, 0.5, 0.0),
         1.4: (0.4, 0.4, 0.6),
         1.6: (0.2, 0.6, 0.2),
         1.8: (0.6, 0.2, 0.0),
         2.0: (1.0, 0.1, 0.0)
    }
    keys = {
         0.0: (1.0, 0.0, 0.0),
         0.2: (2.0, 0.6, 0.0),
         0.4: (0.0, 1.25, 0.0),
         0.6: (0.0, 1.25, 1.0),
         0.8: (0.0, 0.8, 2.0),
         1.0: (0.0, 0.0, 2.0),
         1.2: (0.5, 0.5, 0.0),
         1.4: (0.4, 0.4, 0.6),
         1.6: (0.2, 0.6, 0.2),
         1.8: (0.6, 0.2, 0.0),
         2.0: (1.0, 0.1, 0.0)
        }.items()
        
    def _changecolor(color: Sequence[float]) -> None:
        if self.node.exists():
            self.node.color = color

    for time, color in keys:
        bs.animate_array(self.node, "highlight", 3, animate, loop=True)
        bs.timer(time, bs.Call(_changecolor, highlight))
           
def apply_effect(self, eff: str) -> None:
    if eff == 'fire':
        call = bs.Call(_fire, self)
        self._cm_effect_timer = bs.Timer(0.001, call, repeat=True)
    elif eff == 'particle':
        call = bs.Call(_particle, self)
        self._cm_effect_timer = bs.Timer(0.005, call, repeat=True)
    elif eff == 'smoke':
        call = bs.Call(_smoke, self)
        self._cm_effect_timer = bs.Timer(0.001, call, repeat=True)
    elif eff == 'hole':
        call = bs.Call(_hole, self)
        self._cm_effect_timer = bs.Timer(0.001, call, repeat=True)
    elif eff == 'footprint':
        call = bs.Call(footprint, self)
        self._cm_effect_timer = bs.Timer(0.05, call, repeat=True)
    elif eff == 'stars':
        call = bs.Call(stars, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'spark':
        call = bs.Call(spark, self)
        self._cm_effect_timer = bs.Timer(0.05, call, repeat=True)
    elif eff == 'darkmagic':
        call = bs.Call(darkmagic, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'rainbow':
        call = bs.Call(_rainbow, self)
        self._cm_effect_timer = bs.Timer(1, call, repeat=True)
    elif eff == 'loops':
        loops(self)
    
# -----------

def filter_chat_message(msg: str, client_id: int) -> None:
    command = Commands(msg, client_id, msg.split(' '))
    return command.get
    
def new_ga_on_transition_in(self) -> None:
    calls['GA_OnTransitionIn'](self)
    bui.set_party_icon_always_visible(True)
    Uts.create_data_text(self)
    Uts.create_live_chat(self, live=False)
    try:
        Uts._name_watchdog_timer = bs.Timer(
            1.0 / 60.0, Uts.refresh_permanent_names, repeat=True)
    except Exception:
        pass

def new_on_player_join(self, player: bs.Player) -> None:
    calls['OnPlayerJoin'](self, player)
    Uts.player_join(player)
    Uts.update_usernames()
    Uts.refresh_permanent_names()

def new_playerspaz_init_(self, *args, **kwargs) -> None:
    calls['PlayerSpazInit'](self, *args, **kwargs)
    Uts.update_usernames()
    try:
        sessionplayer = self._player.sessionplayer
        c_id = sessionplayer.inputdevice.client_id
        user = sessionplayer.get_v1_account_id()
    except (AttributeError, ba.SessionPlayerNotFoundError):
        sessionplayer = None
        c_id = None
        user = None
    if c_id is not None and sessionplayer is not None:
        Uts.players[c_id] = sessionplayer
        if user is not None:
            Uts.userpbs[c_id] = user
            if user not in Uts.pdata:
                Uts.add_player_data(user)
            Uts.accounts[c_id] = Uts.pdata[user]
        account = Uts._resolve_account(c_id)
        if account is not None:
            apply_effect(self, account.get('Effect', 'None'))
            stored_name = account.get('Name', 'None')
            if stored_name and stored_name != 'None':
                CommandFunctions.apply_permanent_name(c_id, stored_name)

def new_playerspaz_on_jump_press(self) -> None:    
    calls['OnJumpPress'](self)

    if getattr(self, '_cm_fly', False):
        CommandFunctions.fly_jump_boost(self)

    if not getattr(self, 'cm_superjump', False):
        return
        
    if (not self.node or not self.node.jump_pressed):
        return
    
    msg =  bs.HitMessage(pos=self.node.position,
                            velocity=self.node.velocity,
                            magnitude=300,
                            hit_subtype='imp',
                            radius=20)
                          
    if isinstance(msg, bs.HitMessage):
        for i in range(2):
            with act().context:
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
        
# -----------

class suffertnt(bs.Actor):
    def __init__(self, pos: Sequence[float] = (0.0, 1.0, 0.0)) -> None:
        super().__init__()
        
        shared = SharedObjects.get()
        tex = bs.gettexture('tnt')
        mesh = bs.getmesh('crate')
        position = (pos[0], pos[1] + 1.5, pos[2])
        
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={'body': 'sphere',
                   'position': position,
                   'mesh': mesh,
                   'shadow_size': 0.5,
                   'color_texture': tex,
                   'reflection': 'character',
                   'reflection_scale': [1.0],
                   'materials': [shared.object_material]})
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)


class ExplosiveGift(bs.Actor):
    def __init__(self,
                 time: float = 3.0,
                 owner: bs.Node = None):
        super().__init__()
        
        self.time = time
        self.owner = owner
        self.scale = 0.8
        self.touch = False
        
        pos = list(owner.position)
        velocity = (0.0, 60, 0.0)
        position = (pos[0], pos[1]+1.47, pos[2])
                     
        tex = bs.gettexture('crossOutMask')
        mesh = bs.getmesh('box')
                     
        self.node = bs.newnode('bomb',
                               delegate=self,
                               attrs={'body': 'sphere',
                                      'position': position,
                                      'velocity': velocity,
                                      'mesh': mesh,
                                      'body_scale': self.scale,
                                      'shadow_size': 0.3,
                                      'color_texture': tex,
                                      'sticky': True,
                                      'owner': owner,
                                      'reflection': 'soft',
                                      'reflection_scale': [0.22]})
        bs.animate(self.node, 'mesh_scale',
           {0: 0,
            0.2: self.scale * 1.3,
            0.26: self.scale})
        bs.animate(self.node, 'fuse_length', {0.0: 1.0, time: 0.0})
        bs.timer(time, self._xplosion)
        
    def _xplosion(self):
        radius = 3.0
        shared = SharedObjects.get()
        
        mat = bs.Material()
        mat.add_actions(
            conditions=(
                ('they_have_material', shared.player_material), 'or',
                ('they_have_material', shared.object_material)
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self.call)
            ))
        
        rmats = [mat, shared.attack_material]

        region = bs.newnode('region',
            delegate=self,
            owner=self.node,
            attrs={'scale': tuple(radius*0.7 for s in range(3)),
                   'type': 'sphere',
                   'materials': rmats})
        self.node.connectattr('position', region, 'position')
        
        shield = bs.newnode('shield',
            owner=region,
                attrs={'color': (2.0, 1.0, 0.0),
                       'radius': radius})
        region.connectattr('position', shield, 'position')
        
        bs.getsound('explosion03').play(1, self.node.position)
        bs.timer(0.1, bs.Call(
            self.handlemessage, bs.DieMessage()))
        
    def call(self) -> None:
        node = bs.getcollision().opposingnode
        
        def action():
            #if node != self.owner or node != self.node:
                msg = bs.HitMessage(
                    pos=self.node.position,
                    velocity=node.velocity,
                    magnitude=1200 * 5,
                    radius=800 * 5)

                node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])

        if not self.touch:
            self.touch = True
        else:
            action()
            self.touch = False
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)

class MagicBox(bs.Actor):
    def __init__(self, pos: Sequence[float] = (0.0, 1.0, 0.0)) -> None:
        super().__init__()
        
        shared = SharedObjects.get()
        tex = bs.gettexture('rgbStripes')
        mesh = bs.getmesh('powerup')
        position = (pos[0], pos[1] + 1.5, pos[2])
        
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={'body': 'box',
                   'position': position,
                   'mesh': mesh,
                   'shadow_size': 0.5,
                   'color_texture': tex,
                   'reflection': 'powerup',
                   'reflection_scale': [1.0],
                   'materials': [shared.object_material]})
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PickedUpMessage):
            self.node.gravity_scale = -1.0
        elif isinstance(msg, bs.DroppedMessage):
            self.node.gravity_scale = 1.0
        elif isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)



class Uts:
    directory_user: str = bs.app.env.python_directory_user
    directory_sys: str = directory_user + '/sys/' + bs.app.env.version
    sm: Callable = bs.broadcastmessage
    cm: Callable = bs.chatmessage
    key: str = '#Bsline'
    mod: Any
    accounts: dict[int, Any] = {}
    usernames: dict[int, str] = {}
    shortnames: dict[int, str] = {}
    useraccounts: dict[int, str] = {}
    userpbs: dict[int, str] = {}
    players: dict[int, bs.SessionPlayer] = {}
    _name_watchdog_timer: Any = None

    def _resolve_account(c_id: int, account_name: str = None):
        acc = Uts.accounts.get(c_id)
        if acc is not None:
            return acc
        account_id = Uts.userpbs.get(c_id)
        if account_id is None:
            sessionplayer = Uts.players.get(c_id)
            if sessionplayer is not None:
                try:
                    account_id = sessionplayer.get_v1_account_id()
                except Exception:
                    account_id = None
        if account_id is not None:
            Uts.userpbs[c_id] = account_id
            if account_id not in Uts.pdata:
                Uts.add_player_data(account_id)
            Uts.accounts[c_id] = Uts.pdata[account_id]
            return Uts.accounts[c_id]
        if account_name is None:
            sessionplayer = Uts.players.get(c_id)
            if sessionplayer is not None:
                try:
                    account_name = sessionplayer.inputdevice.get_v1_account_name(True)
                except Exception:
                    account_name = None
        if account_name:
            for account_id, data in Uts.pdata.items():
                if account_name in data.get('Accounts', []):
                    Uts.accounts[c_id] = data
                    Uts.userpbs[c_id] = account_id
                    return data
        return None

    def get_display_name(c_id: int, fallback: str = None) -> str:
        acc = Uts._resolve_account(c_id)
        if acc:
            nm = acc.get('Name', 'None')
            if nm and nm != 'None':
                return nm
        if fallback is not None:
            return fallback
        return Uts.usernames.get(c_id, str(c_id))

    def get_user_name(c_id: int) -> str:
        for r in roster():
            if r['client_id'] == c_id:
                if r['players'] == []:
                    return r['display_string']
                else:
                    return r['players'][0]['name_full']
            break
        return 'UNNAMED'

    def sort_list(vals: list, count: int = 3) -> list:
        vals_dict = dict(r=[])
        
        for n in range(len(vals)):
            vals_dict[n] = list()
            
            for c in vals:
                if len(vals_dict[n]) == count:
                    break
                else:
                    if c not in vals_dict['r']:
                        vals_dict['r'].append(c)
                        vals_dict[n].append(c)
        
            if len(vals_dict['r']) == len(vals):
                vals_dict.pop('r')
                break

        return list(vals_dict.values())

    def colors() -> dict[str, Sequence[float]]:
        return dict(
                زرد=(2.0, 2.0, 0.0),
                کرمی=(2.5, 2.5, 1.8),
                قرمز=(1.5, 0.0, 0.0),
                سبز=(0.0, 1.5, 0.0),
                ابی=(0.3, 0.3, 1.5),
                اسمونی=(0.0, 2.0, 2.0),
                صورتی=(3, 1.2, 1.5),
                نارنجی=(3.0, 1.5, 0.0),
                بنفش=(1.5, 0.75, 3.0),
                سفید=(1.5, 1.5, 1.5),
                سیاه=(0.01, 0.01, 0.01))

    def get_admins() -> list[str]:
        admins = []
        if len(Uts.pdata) > 0:
            for p, d in Uts.pdata.items():
                if d['Admin']:
                    admins.append(p)
        return admins

    def add_or_del_user(c_id: int, add: bool = True) -> None:
        if c_id == -1:
            return Uts.sm(getlanguage('You Are Amazing', subs=c_id), color=(0.5, 0, 1), clients=[c_id], transient=True)
            
        if c_id not in Uts.userpbs:
            Uts.sm(getlanguage('User Invalid', subs=c_id), clients=[c_id], transient=True)
        else:
            user = Uts.userpbs[c_id]
            if add:
                if user in Uts.pdata:
                    if not Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(getlanguage('Add Admin Msg', subs=Uts.usernames[c_id]))
            else:
                if user in Uts.pdata:
                    if Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(getlanguage('Delete Admin Msg', subs=Uts.usernames[c_id]))
            Uts.save_players_data()

    def create_players_data() -> None:
        folder = Uts.directory_user + '/Configs'
        file = folder + '/BslinePlayersData.json'
                
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            Uts.pdata = json.loads(r)

    def save_players_data() -> None:
        folder = Uts.directory_user + '/Configs'
        file = folder + '/BslinePlayersData.json'
        with open(file, 'w') as f:
            w = json.dumps(Uts.pdata, indent=4)
            f.write(w)

    def player_join(player: bs.Player) -> None:
        try:
            sessionplayer = player.sessionplayer
            account_id = sessionplayer.get_v1_account_id()
            client_id = sessionplayer.inputdevice.client_id
            account_name = sessionplayer.inputdevice.get_v1_account_name(True)
        except Exception as e:
            bs.chatmessage(str(e))
            return

        Uts.players[client_id] = sessionplayer
        Uts.useraccounts[client_id] = account_name

        if account_id is not None:
            Uts.userpbs[client_id] = account_id
            if account_id not in Uts.pdata:
                Uts.add_player_data(account_id)
                Uts.sm(getlanguage('Guardando Informacion'),
                       color=(0.35, 0.7, 0.1), transient=True,
                       clients=[client_id])
            accounts = Uts.pdata[account_id].setdefault('Accounts', [])
            if account_name and account_name not in accounts:
                accounts.append(account_name)
                Uts.save_players_data()
            Uts.accounts[client_id] = Uts.pdata[account_id]
        else:
            Uts._resolve_account(client_id, account_name)

        Uts.usernames[client_id] = Uts.get_display_name(
            client_id, fallback=account_name)
        Uts.shortnames[client_id] = Uts.usernames[client_id]

    def update_usernames() -> None:
        for r in roster():
            c_id = r['client_id']
            account_id = r.get('account_id')
            if account_id is not None:
                Uts.userpbs[c_id] = account_id
                if account_id in Uts.pdata:
                    Uts.accounts[c_id] = Uts.pdata[account_id]
            if c_id not in Uts.usernames:
                Uts.usernames[c_id] = r.get('display_string', str(c_id))
            Uts._resolve_account(c_id, r.get('display_string'))

        for c_id, p in list(Uts.players.items()):
            try:
                if not p.exists():
                    continue
                account_id = p.get_v1_account_id()
                if account_id is not None:
                    Uts.userpbs[c_id] = account_id
                    if account_id not in Uts.pdata:
                        Uts.add_player_data(account_id)
                    Uts.accounts[c_id] = Uts.pdata[account_id]
                Uts.usernames[c_id] = p.getname(full=True)
                Uts.shortnames[c_id] = p.getname(full=False)
            except Exception:
                pass

        for c_id in list(Uts.players.keys()):
            dn = Uts.get_display_name(c_id)
            Uts.usernames[c_id] = dn
            Uts.shortnames[c_id] = dn

    @staticmethod
    def refresh_permanent_names() -> None:
        try:
            activity = act()
            if activity is None or isinstance(activity, MainMenuActivity):
                return
            players = getattr(activity, 'players', [])
        except Exception:
            return
        for player in list(players):
            try:
                sessionplayer = player.sessionplayer
                c_id = sessionplayer.inputdevice.client_id
                Uts.players[c_id] = sessionplayer
                account_id = sessionplayer.get_v1_account_id()
                if account_id is not None:
                    Uts.userpbs[c_id] = account_id
                    if account_id not in Uts.pdata:
                        Uts.add_player_data(account_id)
                    Uts.accounts[c_id] = Uts.pdata[account_id]
                account = Uts._resolve_account(c_id)
                if not account:
                    continue
                name = account.get('Name', 'None')
                if not name or name == 'None':
                    continue
                Uts.usernames[c_id] = name
                Uts.shortnames[c_id] = name
                actor = getattr(player, 'actor', None)
                if actor is not None and getattr(actor, 'node', None) is not None:
                    if actor.node.exists():
                        CommandFunctions.apply_permanent_name(c_id, name)
            except Exception:
                pass

    def add_player_data(account_id: str) -> None:
        if account_id not in Uts.pdata:
            Uts.pdata[account_id] = {
                'Mute': False,
                'Effect': 'None',
                'Name': 'None',
                'Admin': False,
                'Accounts': []}
            Uts.save_players_data()

    def save_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/BslineSettings.json'
        
        with open(file, 'w') as f:
            w = json.dumps(cfg, indent=4)
            f.write(w)

    def create_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/BslineSettings.json'
        
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            cfg = json.loads(r)

    def create_user_system_scripts() -> None:

        import shutil
        
        app = bs.app

        if app.python_directory_user is None:
            raise RuntimeError('user python dir unset')
        if app.python_directory_app is None:
            raise RuntimeError('app python dir unset')
    
        path = app.python_directory_user + '/sys/' + app.version
        pathtmp = path
        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(pathtmp):
            shutil.rmtree(pathtmp)
    
        def _ignore_filter(src: str, names: Sequence[str]) -> Sequence[str]:
            del src, names  # Unused
    
            return ('__pycache__',)
    
        print(f'COPYING "{app.python_directory_app}" -> "{pathtmp}".')
        shutil.copytree(app.python_directory_app, pathtmp, ignore=_ignore_filter)
    
        print(f'MOVING "{pathtmp}" -> "{path}".')
        shutil.move(pathtmp, path)
        print(
            f"Created system scripts at :'{path}"
            f"'\nRestart {bui.appname()} to use them."
            f' (use babase.quit() to exit the game)'
        )
        if app.classic is not None and app.classic.platform == 'android':
            print(
                'Note: the new files may not be visible via '
                'android-file-transfer until you restart your device.'
            )
        
    def create_data_text(self) -> None:
        if isinstance(act(), MainMenuActivity):
            return

        if getattr(self, '_text_data', None):
            self._text_data.node.delete()

        if cfg['Commands'].get('ShowInfo'):
            info = getlanguage('Party Info', subs=[
                cfg['Commands'].get('HostName', '???'),
                cfg['Commands'].get('Description', '???')])
            color = tuple(list(cfg['Commands'].get('InfoColor', Uts.colors()['سفید'])) + [1])
                
            self._text_data = text.Text(info,
                position=(-650.0, -200.0), color=color)

    def create_live_chat(self,
                         live: bool = True,
                         chat: list[int, str] = None,
                         admin: bool = False) -> None:
        if isinstance(act(), MainMenuActivity):
            return
        
        if getattr(self, '_live_chat', None):
            self._live_chat.node.delete()
            
        if cfg['Commands'].get('ChatLive'):
            max = 6
            chats = list()
            txt = str()
            icon = bui.charstr(bui.SpecialChar.googlePlayGames_logo) if admin else ''
            
            if any(bs.get_chat_messages()):
                if len(Chats) == max:
                    Chats.pop(0)
                    
                if live:
                    name = Uts.shortnames.get(chat[0], chat[0])
                    msg = chat[1]
                    Chats.append(f'{icon}{name}: {msg}')
                
                for msg in Chats:
                    if len(chats) != max:
                        chats.append(msg)
                    else: break
                txt = '\n'.join(chats)
            
            livetext = getlanguage('Chat Live')
            txt = (livetext + '\n' + ''.join(['=' for s 
                in range(len(livetext))]) + '\n') + txt

            self._live_chat = text.Text(txt, position=(650.0, 200.0),
                color=(1, 1, 1, 1), h_align=text.Text.HAlign.RIGHT)

    def funtion() -> str:
        return """    %s
    try:
        cm = babase.app.bsline_filter_chat(msg, client_id)
        if cm == '@':
            return None
    except Exception:
        pass
        """ % Uts.key








def _install() -> None:
    from bascenev1 import _hooks
    from babase import _app, modutils

    _file = Uts.directory_sys + '/bascenev1/_hooks.py'
    bs.app.bsline_filter_chat = filter_chat_message

    def seq():
        bs.screenmessage(getlanguage('Installing'))
        bs.screenmessage("Success\n\nWelcome Admin", color=(1,1,0))

        bs.apptimer(2.0, bs.Call(
            Uts.sm, getlanguage('Installed'), (0.0, 1.0, 0.0)))
        
        bs.apptimer(4.0, bs.Call(
            Uts.sm, getlanguage('Restart Msg')))
        
        bs.apptimer(6.0, bui.quit)
    
    if not os.path.exists(Uts.directory_sys):
        Uts.create_user_system_scripts()
        bs.apptimer(1.0, bs.Call(
            bs.screenmessage, getlanguage('Make Sys'), (0.0, 1.0, 0.0)))
        seq()
        del seq

    with open(_file) as s:
        read = s.read()
        read_l = read.split('\n')
        
    if Uts.key not in read:
        f_list = Uts.funtion().split('\n')
        ix = read_l.index('def filter_chat_message(msg: str, client_id: int) -> str | None:')
        
        for i, lt in enumerate(f_list):
            read_l.insert(i+(ix+1), lt)

        read = '\n'.join(read_l)
        with open(_file, 'w') as s:
            s.write(read)
        seq()

    Uts.create_players_data()
    #Uts.add_admin('pb-IF4XLRUN')
    Uts.save_players_data()

def settings():
    global cfg
    Uts.create_settings()
    
    if cfg.get('Commands') is None:
        cfg['Commands'] = dict()
        Uts.save_settings()
 
def plugin():
    calls['GA_OnTransitionIn'] = bs.GameActivity.on_transition_in
    calls['OnJumpPress'] = PlayerSpaz.on_jump_press
    calls['OnPlayerJoin'] = Activity.on_player_join
    calls['PlayerSpazInit'] = PlayerSpaz.__init__

    
    bs.GameActivity.on_transition_in = new_ga_on_transition_in
    PlayerSpaz.on_jump_press = new_playerspaz_on_jump_press
    Activity.on_player_join = new_on_player_join
    PlayerSpaz.__init__ = new_playerspaz_init_
    bui.set_party_icon_always_visible(True)

# ba_meta export plugin
class Install(bs.Plugin):
    def __init__(self):
        plugin()
        settings()
        bs.apptimer(1.3, _install)
####