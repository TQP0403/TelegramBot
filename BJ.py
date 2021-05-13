### BLACKJACK ###
global sender_id
global card_list
global my_card
global is_playing
global dealer_card
import random

sender_id = ""
card_list = [2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,10,10,10,10]
my_card = []
is_playing = False
on_hand = 0
dealer_hand = 0

# START GAME
if message_content.startswith('blackjack') and client.user.mentioned_in(message) and is_playing == False:

    is_playing = True
    sender_id = str(message.author.id)

    if sender_id not in db.keys():
        db[sender_id] = 1000

    await message.channel.send(
        f"{message.author.mention}'s account currently have {db[sender_id]} P-Coin(s). Default bet is 100.")

    my_card = random.sample(card_list, 2)

    await message.channel.send(f'Game start!')
    await message.channel.send(f'On hand: {my_card}\nTotal: {sum(my_card)}')
    await message.channel.send('Choose: Hit or Stay?')

# HIT
if message_content == 'hit' and is_playing == True:
    my_card.append(random.choice(card_list))
    await message.channel.send(f'on hand: {my_card}, total: {sum(my_card)}')
    if sum(my_card) > 21:
        db[sender_id] -= 100
        await message.channel.send(f'BUSTED! Better luck next time ;)\n-100 P-Coins (remaining: {db[sender_id]})')
        is_playing = False
    if sum(my_card) == 21:
        db[sender_id] += 150
        await message.channel.send(f'BLACKJACK! Very niceee :>\n+150 P-Coins (remaining: {db[sender_id]})')
        is_playing = False
    if sum(my_card) < 21:
        await message.channel.send('Choose: Hit or Stay?')

# STAY
if message_content == 'stay' and is_playing == True:
    dealer_card = random.sample(card_list, 2)
    while sum(dealer_card) < sum(my_card):
        dealer_card.append(random.choice(card_list))
    await message.channel.send(f'On hand: {my_card}\nTotal: {sum(my_card)}')
    await message.channel.send(f'Dealer hand: {dealer_card}\nTotal: {sum(dealer_card)}')

    if sum(dealer_card) > sum(my_card) and sum(dealer_card) <= 21:
        db[sender_id] -= 100
        await message.channel.send(f'U LOSE! Better luck next time ;)\n-100 P-Coins (remaining: {db[sender_id]})')
    if sum(dealer_card) < sum(my_card) or sum(dealer_card) > 21:
        db[sender_id] += 100
        await message.channel.send(f'U WIN!:3\n+100 P-Coins (remaining: {db[sender_id]})')
    if sum(dealer_card) == sum(my_card):
        await message.channel.send('DRAW :v')

    is_playing = False